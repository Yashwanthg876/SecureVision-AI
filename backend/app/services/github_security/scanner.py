import re
import uuid
import time
import logging
import asyncio
import httpx
from urllib.parse import urlsplit
from datetime import datetime
from typing import List, Tuple, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.schemas.github_security import (
    GitHubScanResponse, RepoInfo, SecretFinding,
    DependencyFinding, RiskyFileFinding
)
from app.repositories.github_scan_repository import github_scan_repository
import json

logger = logging.getLogger(__name__)

import os

GITHUB_API = "https://api.github.com"

def _get_github_headers() -> Dict[str, str]:
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

# ─── Secret detection patterns ────────────────────────────────────────────────
SECRET_PATTERNS: List[Dict[str, Any]] = [
    {"name": "AWS Access Key",        "regex": r"AKIA[0-9A-Z]{16}",                          "severity": "Critical"},
    {"name": "AWS Secret Key",        "regex": r"(?i)aws.{0,20}secret.{0,20}['\"][0-9a-zA-Z/+]{40}['\"]", "severity": "Critical"},
    {"name": "GitHub Token",          "regex": r"ghp_[0-9a-zA-Z]{36}",                       "severity": "Critical"},
    {"name": "GitHub OAuth Token",    "regex": r"gho_[0-9a-zA-Z]{36}",                       "severity": "Critical"},
    {"name": "GitHub App Token",      "regex": r"(ghu|ghs|ghr)_[0-9a-zA-Z]{36}",            "severity": "Critical"},
    {"name": "Slack Token",           "regex": r"xox[baprs]-[0-9a-zA-Z\-]{10,48}",           "severity": "High"},
    {"name": "Stripe Secret Key",     "regex": r"sk_live_[0-9a-zA-Z]{24,}",                  "severity": "Critical"},
    {"name": "Stripe Test Key",       "regex": r"sk_test_[0-9a-zA-Z]{24,}",                  "severity": "High"},
    {"name": "Google API Key",        "regex": r"AIza[0-9A-Za-z\-_]{35}",                    "severity": "High"},
    {"name": "SendGrid API Key",      "regex": r"SG\.[0-9A-Za-z\-_]{22}\.[0-9A-Za-z\-_]{43}", "severity": "High"},
    {"name": "Twilio Auth Token",     "regex": r"(?i)twilio.{0,20}['\"][0-9a-f]{32}['\"]",   "severity": "High"},
    {"name": "Private Key",           "regex": r"-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----", "severity": "Critical"},
    {"name": "Generic Secret",        "regex": r"(?i)(secret|password|passwd|api_key|apikey|access_token)\s*[=:]\s*['\"][^'\"]{8,}['\"]", "severity": "Medium"},
    {"name": "Generic Token",         "regex": r"(?i)(token|auth|bearer)\s*[=:]\s*['\"][^'\"]{16,}['\"]", "severity": "Medium"},
    {"name": "Connection String",     "regex": r"(?i)(mongodb|postgresql|mysql|redis):\/\/[^:]+:[^@]+@", "severity": "High"},
    {"name": "JWT Token",             "regex": r"eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+", "severity": "Medium"},
]

# ─── Risky file patterns ───────────────────────────────────────────────────────
RISKY_FILE_PATTERNS: List[Dict[str, Any]] = [
    {"pattern": r"^\.env$",              "reason": "Environment file may contain secrets",       "severity": "Critical"},
    {"pattern": r"^\.env\.",             "reason": "Environment config file",                     "severity": "High"},
    {"pattern": r"id_rsa$",             "reason": "RSA private key file",                        "severity": "Critical"},
    {"pattern": r"id_dsa$",             "reason": "DSA private key file",                        "severity": "Critical"},
    {"pattern": r"id_ecdsa$",           "reason": "ECDSA private key file",                      "severity": "Critical"},
    {"pattern": r"id_ed25519$",         "reason": "Ed25519 private key file",                    "severity": "Critical"},
    {"pattern": r"\.pem$",              "reason": "PEM certificate/key file",                    "severity": "High"},
    {"pattern": r"\.p12$",              "reason": "PKCS12 certificate/key bundle",               "severity": "High"},
    {"pattern": r"\.pfx$",              "reason": "Personal Information Exchange file",           "severity": "High"},
    {"pattern": r"\.key$",              "reason": "Cryptographic key file",                      "severity": "High"},
    {"pattern": r"secrets\.ya?ml$",     "reason": "Secrets configuration file",                  "severity": "Critical"},
    {"pattern": r"credentials\.json$",  "reason": "Credentials file",                            "severity": "Critical"},
    {"pattern": r"\.htpasswd$",         "reason": "htpasswd credentials file",                   "severity": "High"},
    {"pattern": r"wp-config\.php$",     "reason": "WordPress config with DB credentials",        "severity": "High"},
    {"pattern": r"database\.yml$",      "reason": "Database configuration file",                 "severity": "Medium"},
    {"pattern": r"config\.php$",        "reason": "PHP configuration file",                      "severity": "Medium"},
    {"pattern": r"\.npmrc$",            "reason": "npm config may contain auth tokens",          "severity": "Medium"},
    {"pattern": r"\.pypirc$",           "reason": "PyPI config may contain credentials",         "severity": "Medium"},
    {"pattern": r"settings\.py$",       "reason": "Django settings file",                        "severity": "Medium"},
    {"pattern": r"application\.properties$", "reason": "Spring Boot app config",                 "severity": "Medium"},
]

# ─── Dependency file patterns ──────────────────────────────────────────────────
DEPENDENCY_FILES: List[Dict[str, str]] = [
    {"pattern": r"package\.json$",       "type": "npm",    "description": "Node.js dependency manifest"},
    {"pattern": r"requirements\.txt$",   "type": "pip",    "description": "Python pip dependencies"},
    {"pattern": r"Pipfile$",             "type": "pipenv", "description": "Python Pipenv manifest"},
    {"pattern": r"pom\.xml$",            "type": "maven",  "description": "Java Maven dependency file"},
    {"pattern": r"build\.gradle$",       "type": "gradle", "description": "Gradle build file"},
    {"pattern": r"Gemfile$",             "type": "gem",    "description": "Ruby gem dependencies"},
    {"pattern": r"composer\.json$",      "type": "composer","description": "PHP Composer manifest"},
    {"pattern": r"go\.mod$",             "type": "go",     "description": "Go module dependencies"},
    {"pattern": r"Cargo\.toml$",         "type": "cargo",  "description": "Rust Cargo manifest"},
    {"pattern": r"yarn\.lock$",          "type": "yarn",   "description": "Yarn lockfile"},
    {"pattern": r"package-lock\.json$",  "type": "npm",    "description": "npm lockfile"},
]

# ─── Files to skip scanning (binary / large / generated) ──────────────────────
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg", ".webp", ".bmp",
    ".mp4", ".mp3", ".wav", ".pdf", ".zip", ".tar", ".gz", ".rar",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".woff", ".woff2", ".ttf",
    ".eot", ".lock", ".min.js", ".min.css", ".map",
}


def _parse_repo_url(url: str) -> Tuple[str, str]:
    """Extract owner and repo name from a GitHub URL."""
    parsed = urlsplit(url.strip())
    if parsed.scheme != "https" or (parsed.hostname or "").lower() != "github.com":
        raise ValueError("Repository URL must use https://github.com/owner/repository")
    if parsed.username or parsed.password or parsed.port is not None or parsed.query or parsed.fragment:
        raise ValueError("Invalid GitHub repository URL")
    parts = [part for part in parsed.path.rstrip("/").split("/") if part]
    if len(parts) != 2:
        raise ValueError("Repository URL must identify one owner and repository")
    owner, repo = parts
    repo = re.sub(r"\.git$", "", repo, flags=re.IGNORECASE)
    valid_slug = re.compile(r"^[A-Za-z0-9_.-]+$")
    if not valid_slug.fullmatch(owner) or not valid_slug.fullmatch(repo) or repo in {".", ".."}:
        raise ValueError("Invalid GitHub owner or repository name")
    return owner, repo


def _should_skip(path: str) -> bool:
    lower = path.lower()
    for ext in SKIP_EXTENSIONS:
        if lower.endswith(ext):
            return True
    # Skip common vendor/generated dirs
    skip_dirs = ("node_modules/", "vendor/", ".git/", "dist/", "build/", "__pycache__/", ".next/")
    for d in skip_dirs:
        if d in lower:
            return True
    return False


def _check_risky_files(files: List[str]) -> List[RiskyFileFinding]:
    findings = []
    for path in files:
        filename = path.split("/")[-1]
        for rule in RISKY_FILE_PATTERNS:
            if re.search(rule["pattern"], filename, re.IGNORECASE):
                findings.append(RiskyFileFinding(
                    file_path=path,
                    risk_reason=rule["reason"],
                    severity=rule["severity"],
                ))
                break  # one match per file
    return findings


def _check_dependency_files(files: List[str]) -> List[DependencyFinding]:
    findings = []
    for path in files:
        filename = path.split("/")[-1]
        for rule in DEPENDENCY_FILES:
            if re.search(rule["pattern"], filename, re.IGNORECASE):
                findings.append(DependencyFinding(
                    file_path=path,
                    dependency_type=rule["type"],
                    description=rule["description"],
                    severity="Low",
                    recommendation=(
                        f"Review {rule['type']} dependencies for known vulnerabilities. "
                        "Run a dependency audit (e.g., `npm audit`, `pip-audit`) and pin versions."
                    ),
                ))
                break
    return findings


async def _scan_file_for_secrets(
    client: httpx.AsyncClient,
    owner: str,
    repo: str,
    path: str,
    branch: str,
    semaphore: asyncio.Semaphore,
) -> List[SecretFinding]:
    """Fetch a raw file from GitHub and regex-scan it for secrets."""
    findings = []
    raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{path}"
    async with semaphore:
        try:
            resp = await client.get(raw_url, timeout=5.0)
            if resp.status_code != 200:
                return []
            content = resp.text
            # Skip files that are too large (>100KB)
            if len(content) > 100_000:
                return []
            for pattern in SECRET_PATTERNS:
                if re.search(pattern["regex"], content):
                    findings.append(SecretFinding(
                        file_path=path,
                        pattern_name=pattern["name"],
                        severity=pattern["severity"],
                        description=f"Potential {pattern['name']} detected in `{path}`.",
                        recommendation=(
                            "Immediately revoke and rotate this credential. "
                            "Remove it from the codebase and use environment variables or a secrets manager instead. "
                            "Consider using git-secrets or truffleHog in your CI pipeline."
                        ),
                    ))
        except Exception as e:
            logger.debug(f"Could not fetch {path}: {e}")
    return findings


def _calculate_score(
    secret_findings: List[SecretFinding],
    risky_files: List[RiskyFileFinding],
) -> Tuple[int, str]:
    """Calculate a 0–100 security score and risk level."""
    score = 100
    for s in secret_findings:
        if s.severity == "Critical":
            score -= 25
        elif s.severity == "High":
            score -= 15
        elif s.severity == "Medium":
            score -= 8
        else:
            score -= 3

    for r in risky_files:
        if r.severity == "Critical":
            score -= 15
        elif r.severity == "High":
            score -= 8
        elif r.severity == "Medium":
            score -= 4
        else:
            score -= 2

    score = max(0, min(100, score))

    if score >= 85:
        risk = "Low"
    elif score >= 65:
        risk = "Medium"
    elif score >= 40:
        risk = "High"
    else:
        risk = "Critical"

    return score, risk


class GitHubSecurityScanner:
    async def scan(self, repo_url: str, db: Session, user_id: str) -> GitHubScanResponse:
        start_ms = int(time.time() * 1000)
        owner, repo_name = _parse_repo_url(repo_url)

        async with httpx.AsyncClient(headers=_get_github_headers(), follow_redirects=True) as client:
            # ── 1. Fetch repo metadata ────────────────────────────────────────
            repo_resp = await client.get(f"{GITHUB_API}/repos/{owner}/{repo_name}", timeout=10.0)
            if repo_resp.status_code == 404:
                raise ValueError(f"Repository '{owner}/{repo_name}' not found or is private.")
            if repo_resp.status_code == 403:
                raise ValueError("GitHub API rate limit exceeded. Please try again in a few minutes.")
            if repo_resp.status_code != 200:
                raise ValueError(f"GitHub API error: {repo_resp.status_code}")

            repo_data = repo_resp.json()
            default_branch = repo_data.get("default_branch", "main")

            repo_info = RepoInfo(
                full_name=repo_data.get("full_name", f"{owner}/{repo_name}"),
                description=repo_data.get("description"),
                default_branch=default_branch,
                is_private=repo_data.get("private", False),
                language=repo_data.get("language"),
                topics=repo_data.get("topics", []),
                stars=repo_data.get("stargazers_count", 0),
                forks=repo_data.get("forks_count", 0),
                open_issues=repo_data.get("open_issues_count", 0),
                created_at=repo_data.get("created_at", ""),
                updated_at=repo_data.get("updated_at", ""),
                size_kb=repo_data.get("size", 0),
                license=repo_data.get("license", {}).get("name") if repo_data.get("license") else None,
            )

            # ── 2. Fetch file tree ────────────────────────────────────────────
            tree_resp = await client.get(
                f"{GITHUB_API}/repos/{owner}/{repo_name}/git/trees/{default_branch}?recursive=1",
                timeout=15.0,
            )
            if tree_resp.status_code == 403:
                raise ValueError("GitHub API rate limit exceeded. Please try again in a few minutes.")

            all_files: List[str] = []
            if tree_resp.status_code == 200:
                tree_data = tree_resp.json()
                all_files = [
                    item["path"]
                    for item in tree_data.get("tree", [])
                    if item.get("type") == "blob"
                ]

            # ── 3. Classify files ─────────────────────────────────────────────
            risky_files = _check_risky_files(all_files)
            dep_findings = _check_dependency_files(all_files)

            # ── 4. Scan text files for secrets (concurrent, max 40 files) ────
            scannable = [
                f for f in all_files
                if not _should_skip(f)
            ][:40]

            # Use a semaphore to limit to 10 concurrent requests
            semaphore = asyncio.Semaphore(10)
            tasks = [
                _scan_file_for_secrets(client, owner, repo_name, path, default_branch, semaphore)
                for path in scannable
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            secret_findings: List[SecretFinding] = []
            for result in results:
                if isinstance(result, list):
                    secret_findings.extend(result)

        # ── 5. Score & risk ───────────────────────────────────────────────────
        score, risk_level = _calculate_score(secret_findings, risky_files)

        def count_by_severity(items, attr="severity"):
            counts = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0}
            for item in items:
                sev = getattr(item, attr, "Low")
                if sev in counts:
                    counts[sev] += 1
            return counts

        secret_sev = count_by_severity(secret_findings)
        risky_sev  = count_by_severity(risky_files)
        dep_sev    = count_by_severity(dep_findings)

        critical = secret_sev["Critical"] + risky_sev["Critical"]
        high     = secret_sev["High"]     + risky_sev["High"]
        medium   = secret_sev["Medium"]   + risky_sev["Medium"]
        low      = secret_sev["Low"]      + risky_sev["Low"] + len(dep_findings)

        scan_id = str(uuid.uuid4())
        duration_ms = int(time.time() * 1000) - start_ms

        result = GitHubScanResponse(
            id=scan_id,
            repo_url=repo_url,
            repo_name=repo_name,
            owner=owner,
            risk_level=risk_level,
            security_score=score,
            total_files_scanned=len(scannable),
            secrets_count=len(secret_findings),
            risky_files_count=len(risky_files),
            dependency_files_count=len(dep_findings),
            critical_count=critical,
            high_count=high,
            medium_count=medium,
            low_count=low,
            repo_info=repo_info,
            secret_findings=secret_findings,
            risky_files=risky_files,
            dependency_findings=dep_findings,
            scan_duration_ms=duration_ms,
            status="Completed",
            created_at=datetime.utcnow().isoformat(),
        )

        # ── 6. Persist to DB ──────────────────────────────────────────────────
        try:
            github_scan_repository.create(db, obj_in={
                "user_id": user_id,
                "repo_url": repo_url,
                "repo_name": repo_name,
                "owner": owner,
                "risk_level": risk_level,
                "security_score": score,
                "total_files_scanned": len(scannable),
                "secrets_count": len(secret_findings),
                "risky_files_count": len(risky_files),
                "dependency_files_count": len(dep_findings),
                "critical_count": critical,
                "high_count": high,
                "medium_count": medium,
                "low_count": low,
                "scan_duration_ms": duration_ms,
                "status": "Completed",
                "result_json": result.model_dump_json(),
            })
        except Exception as e:
            raise RuntimeError("GitHub scan completed but could not be saved") from e

        return result


github_scanner = GitHubSecurityScanner()
