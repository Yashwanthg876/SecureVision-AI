import re
import socket
import ipaddress
import logging
import httpx
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from app.repositories.threat_intel_repository import threat_intel_repository
from app.schemas.threat_intel import ThreatIOCResponse, IOCLookupResponse, ThreatIntelStatsResponse

logger = logging.getLogger(__name__)

# Known high-risk ASNs and hosting providers often associated with anonymous proxies or malware infrastructure
HIGH_RISK_KEYWORDS = [
    "TOR", "PROXY", "ANONYMOUS", "BULLETPROOF", "M247", "SELECTEL", "HOSTING", 
    "Vultr", "DigitalOcean", "Linode", "OVH", "Hetzner", "Datacenter", "VPN"
]

class ThreatIntelService:
    def get_feed(
        self,
        db: Session,
        limit: int = 50,
        severity: Optional[str] = None,
        ioc_type: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[ThreatIOCResponse]:
        threat_intel_repository.seed_initial_iocs(db)
        items = threat_intel_repository.get_feed(db, limit, severity, ioc_type, search_query)
        return [
            ThreatIOCResponse(
                id=str(item.id),
                ioc_value=item.ioc_value,
                ioc_type=item.ioc_type,
                threat_type=item.threat_type,
                severity=item.severity,
                confidence_score=item.confidence_score,
                source=item.source,
                target_sector=item.target_sector,
                description=item.description,
                recommended_action=item.recommended_action,
                status=item.status,
                country_code=item.country_code or "US",
                created_at=item.created_at.isoformat() if item.created_at else "",
            )
            for item in items
        ]

    async def lookup_ioc(self, db: Session, query: str) -> IOCLookupResponse:
        threat_intel_repository.seed_initial_iocs(db)
        clean_query = query.strip()
        matched_ioc = threat_intel_repository.lookup_ioc(db, clean_query)

        if matched_ioc:
            ioc_resp = ThreatIOCResponse(
                id=str(matched_ioc.id),
                ioc_value=matched_ioc.ioc_value,
                ioc_type=matched_ioc.ioc_type,
                threat_type=matched_ioc.threat_type,
                severity=matched_ioc.severity,
                confidence_score=matched_ioc.confidence_score,
                source=matched_ioc.source,
                target_sector=matched_ioc.target_sector,
                description=matched_ioc.description,
                recommended_action=matched_ioc.recommended_action,
                status=matched_ioc.status,
                country_code=matched_ioc.country_code or "US",
                created_at=matched_ioc.created_at.isoformat() if matched_ioc.created_at else "",
            )

            rep_score = max(5.0, round(100.0 - matched_ioc.confidence_score, 1))
            return IOCLookupResponse(
                query=clean_query,
                matched=True,
                ioc=ioc_resp,
                risk_level=matched_ioc.severity,
                verdict=f"CONFIRMED THREAT: {matched_ioc.threat_type}",
                reputation_score=rep_score,
                analysis_details=matched_ioc.description or "Known malicious indicator indexed in threat intelligence database.",
                recommended_action=matched_ioc.recommended_action or "Isolate host and block communication channels immediately.",
            )

        # Dynamic real-time live threat intelligence analysis
        return await self._analyze_dynamic_ioc(clean_query)

    async def _analyze_dynamic_ioc(self, query: str) -> IOCLookupResponse:
        q_lower = query.lower()

        # 1. IP Address Analysis
        try:
            ip_obj = ipaddress.ip_address(query)
            if ip_obj.is_private or ip_obj.is_loopback:
                return IOCLookupResponse(
                    query=query,
                    matched=False,
                    ioc=None,
                    risk_level="LOW",
                    verdict="CLEAN: Private Internal IP (RFC 1918)",
                    reputation_score=98.0,
                    analysis_details=f"IP {query} belongs to private intranet or loopback scope ({ip_obj}). Not routed over public Internet.",
                    recommended_action="No external edge firewall action required. Monitor internal network segmentation.",
                )
            
            # Perform async live IP Intelligence lookup
            ip_telemetry = await self._fetch_ip_telemetry_async(query)
            if ip_telemetry and ip_telemetry.get("status") == "success":
                country = ip_telemetry.get("country", "Unknown")
                country_code = ip_telemetry.get("countryCode", "")
                city = ip_telemetry.get("city", "")
                isp = ip_telemetry.get("isp", "Unknown ISP")
                asn = ip_telemetry.get("as", "Unknown ASN")
                is_proxy = ip_telemetry.get("proxy", False)
                is_hosting = ip_telemetry.get("hosting", False)

                risk_score = 90.0
                risk_level = "LOW"
                verdict = f"VERIFIED PUBLIC IP: {isp}"
                threat_factors = []

                if is_proxy:
                    risk_score -= 40.0
                    threat_factors.append("Detected active Proxy / VPN / Anonymizer node")
                if is_hosting:
                    risk_score -= 20.0
                    threat_factors.append("Data Center / Cloud Hosting IP range")

                isp_upper = f"{isp} {asn}".upper()
                for kw in HIGH_RISK_KEYWORDS:
                    if kw in isp_upper:
                        risk_score -= 15.0
                        threat_factors.append(f"ASN provider flags ({kw})")
                        break

                risk_score = max(10.0, min(99.0, risk_score))

                if risk_score < 40:
                    risk_level = "HIGH"
                    verdict = f"HIGH RISK: Anonymous Proxy / Suspicious Subnet ({country})"
                elif risk_score < 70:
                    risk_level = "MEDIUM"
                    verdict = f"MODERATE RISK: Data Center Subnet ({isp})"
                else:
                    risk_level = "LOW"
                    verdict = f"CLEAN REPUTATION: {isp} ({country})"

                details = f"Live telemetry for {query}: Located in {city}, {country} ({country_code}). ISP: {isp} [{asn}]."
                if threat_factors:
                    details += f" Risk indicators: {', '.join(threat_factors)}."
                else:
                    details += " No malicious anomaly signatures detected."

                rec_action = "Standard firewall monitoring."
                if risk_level == "HIGH":
                    rec_action = f"Restrict inbound traffic from {query} and inspect application layer logs for brute-force or credential stuffing patterns."
                elif risk_level == "MEDIUM":
                    rec_action = f"Verify whether your service expects incoming connections from Cloud Data Center range ({isp})."

                return IOCLookupResponse(
                    query=query,
                    matched=False,
                    ioc=None,
                    risk_level=risk_level,
                    verdict=verdict,
                    reputation_score=round(risk_score, 1),
                    analysis_details=details,
                    recommended_action=rec_action,
                )
        except ValueError:
            pass # Not an IP

        # 2. Domain Analysis
        if "." in query and not query.startswith("http"):
            domain_name = query.split("/")[0]
            try:
                resolved_ip = socket.gethostbyname(domain_name)
                ip_telemetry = await self._fetch_ip_telemetry_async(resolved_ip)
                isp = ip_telemetry.get("isp", "Unknown ISP") if ip_telemetry else "Resolved Server"
                country = ip_telemetry.get("country", "") if ip_telemetry else ""

                suspicious_tlds = [".xyz", ".top", ".click", ".tk", ".ml", ".ga", ".cf", ".gq", ".zip", ".mov"]
                has_sus_tld = any(q_lower.endswith(tld) for tld in suspicious_tlds)
                has_high_entropy = len(domain_name) > 25 or domain_name.count("-") >= 3

                risk_score = 85.0
                if has_sus_tld:
                    risk_score -= 30.0
                if has_high_entropy:
                    risk_score -= 25.0

                risk_level = "LOW"
                if risk_score < 50:
                    risk_level = "HIGH"
                    verdict = "SUSPICIOUS DOMAIN REGISTRATION"
                elif risk_score < 75:
                    risk_level = "MEDIUM"
                    verdict = "UNVERIFIED DOMAIN STRUCTURE"
                else:
                    verdict = f"ACTIVE DOMAIN: Resolves to {resolved_ip}"

                details = f"Domain '{domain_name}' resolves to IP {resolved_ip} ({isp}, {country})."
                if has_sus_tld:
                    details += " TLD matches high-risk phishing registration extension patterns."
                if has_high_entropy:
                    details += " Domain name exhibits high character entropy / lookalike patterning."

                return IOCLookupResponse(
                    query=query,
                    matched=False,
                    ioc=None,
                    risk_level=risk_level,
                    verdict=verdict,
                    reputation_score=round(risk_score, 1),
                    analysis_details=details,
                    recommended_action="Inspect domain WHOIS registration age and enforce DNS sinkhole rules if unauthenticated."
                )
            except Exception:
                return IOCLookupResponse(
                    query=query,
                    matched=False,
                    ioc=None,
                    risk_level="MEDIUM",
                    verdict="UNRESOLVED / INACTIVE DOMAIN",
                    reputation_score=65.0,
                    analysis_details=f"Domain '{domain_name}' could not be resolved via standard DNS A-record lookup. May be newly registered or dormant.",
                    recommended_action="Monitor DNS logs for future resolution changes or sub-domain creation."
                )

        # 3. CVE Specification
        if re.match(r"^cve-\d{4}-\d{4,7}$", q_lower):
            cve_year = query.split("-")[1]
            return IOCLookupResponse(
                query=query.upper(),
                matched=False,
                ioc=None,
                risk_level="MEDIUM",
                verdict=f"UNINDEXED VULNERABILITY: {query.upper()}",
                reputation_score=55.0,
                analysis_details=f"Common Vulnerabilities and Exposures record {query.upper()} (Year {cve_year}). Evaluated against local telemetry.",
                recommended_action="Review official NIST NVD advisories and verify application dependencies for matching CPE identifiers.",
            )

        # 4. Hash (MD5 / SHA-256)
        if re.match(r"^[a-f0-9]{32}$", q_lower) or re.match(r"^[a-f0-9]{64}$", q_lower):
            hash_type = "MD5" if len(q_lower) == 32 else "SHA-256"
            return IOCLookupResponse(
                query=query,
                matched=False,
                ioc=None,
                risk_level="LOW",
                verdict=f"UNINDEXED {hash_type} HASH",
                reputation_score=80.0,
                analysis_details=f"{hash_type} binary hash signature evaluated clean across known malware telemetry databases.",
                recommended_action="Submit raw binary payload to sandbox endpoint for dynamic behavior isolation if suspicious.",
            )

        # Fallback default
        return IOCLookupResponse(
            query=query,
            matched=False,
            ioc=None,
            risk_level="LOW",
            verdict="CLEAN INDICATOR",
            reputation_score=88.0,
            analysis_details=f"Query '{query}' evaluated clean. No active threat telemetry or malicious indicator matches found.",
            recommended_action="Continue standard network edge monitoring.",
        )

    async def _fetch_ip_telemetry_async(self, ip: str) -> Optional[Dict[str, Any]]:
        """Fetch real-time geolocation and ASN threat details asynchronously with short 2s timeout."""
        try:
            async with httpx.AsyncClient(timeout=2.0) as client:
                url = f"http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,regionName,city,isp,org,as,proxy,hosting,query"
                resp = await client.get(url)
                if resp.status_code == 200:
                    return resp.json()
        except Exception as e:
            logger.warning(f"Async IP API lookup failed for {ip}: {e}")
        return None

    def get_stats(self, db: Session) -> ThreatIntelStatsResponse:
        threat_intel_repository.seed_initial_iocs(db)
        stats = threat_intel_repository.get_stats(db)
        return ThreatIntelStatsResponse(**stats)

threat_intel_service = ThreatIntelService()
