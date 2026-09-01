from pydantic import BaseModel, Field
from typing import List, Optional


class GitHubScanRequest(BaseModel):
    repo_url: str = Field(..., min_length=1, max_length=512)


class SecretFinding(BaseModel):
    file_path: str
    pattern_name: str
    severity: str  # Critical, High, Medium, Low
    description: str
    recommendation: str


class DependencyFinding(BaseModel):
    file_path: str
    dependency_type: str  # npm, pip, maven, etc.
    description: str
    severity: str
    recommendation: str


class RiskyFileFinding(BaseModel):
    file_path: str
    risk_reason: str
    severity: str


class RepoInfo(BaseModel):
    full_name: str
    description: Optional[str]
    default_branch: str
    is_private: bool
    language: Optional[str]
    topics: List[str]
    stars: int
    forks: int
    open_issues: int
    created_at: str
    updated_at: str
    size_kb: int
    license: Optional[str]


class GitHubScanResponse(BaseModel):
    id: str
    repo_url: str
    repo_name: str
    owner: str
    risk_level: str          # Critical, High, Medium, Low
    security_score: int      # 0–100
    total_files_scanned: int
    secrets_count: int
    risky_files_count: int
    dependency_files_count: int
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int
    repo_info: RepoInfo
    secret_findings: List[SecretFinding]
    risky_files: List[RiskyFileFinding]
    dependency_findings: List[DependencyFinding]
    scan_duration_ms: int
    status: str
    created_at: str
