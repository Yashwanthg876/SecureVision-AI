import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.repositories.base_repository import BaseRepository
from app.models.threat_intel import ThreatIOC

SEED_THREAT_DATA = [
    {
        "ioc_value": "185.220.101.5",
        "ioc_type": "ip",
        "threat_type": "Ransomware C2",
        "severity": "CRITICAL",
        "confidence_score": 98.5,
        "source": "CISA Cyber Defense Feed",
        "target_sector": "Financial Services & Banking",
        "description": "Known Command & Control server IP associated with LockBit 3.0 ransomware distribution and automated payload staging.",
        "recommended_action": "Block inbound and outbound network traffic to 185.220.101.5 at edge firewall and update perimeter WAF rules immediately.",
        "status": "ACTIVE",
        "country_code": "RU",
    },
    {
        "ioc_value": "cve-2024-3094",
        "ioc_type": "cve",
        "threat_type": "Supply Chain Vulnerability",
        "severity": "CRITICAL",
        "confidence_score": 99.0,
        "source": "NIST NVD & SecureVision AI Core",
        "target_sector": "Global Linux Systems",
        "description": "Backdoor in XZ Utils data compression library allowing unauthorized sshd remote authentication bypass.",
        "recommended_action": "Downgrade xz packages to version 5.4.x or upgrade to verified clean distribution release. Audit SSH authentication logs.",
        "status": "ACTIVE",
        "country_code": "DE",
    },
    {
        "ioc_value": "auth-verify-security-login.com",
        "ioc_type": "domain",
        "threat_type": "Credential Phishing",
        "severity": "HIGH",
        "confidence_score": 92.0,
        "source": "AlienVault OTX & OpenPhish",
        "target_sector": "Cloud SaaS & Enterprise SSO",
        "description": "Newly registered lookalike domain mimicking enterprise OAuth login endpoints for credential harvesting.",
        "recommended_action": "Add domain to DNS sinkhole list and deploy email gateway domain protection filters.",
        "status": "ACTIVE",
        "country_code": "US",
    },
    {
        "ioc_value": "e99a18c428cb38d5f260853678922e03",
        "ioc_type": "hash",
        "threat_type": "Trojan Loader",
        "severity": "HIGH",
        "confidence_score": 94.0,
        "source": "VirusTotal & SecureVision AI",
        "target_sector": "Healthcare & Defense",
        "description": "MD5 hash of obfuscated PowerShell dropper script deploying Cobalt Strike beacon payloads.",
        "recommended_action": "Quarantine matching binaries across endpoints via EDR agent. Restrict PowerShell execution policy.",
        "status": "ACTIVE",
        "country_code": "CN",
    },
    {
        "ioc_value": "194.26.29.112",
        "ioc_type": "ip",
        "threat_type": "Mirai Botnet Node",
        "severity": "MEDIUM",
        "confidence_score": 88.0,
        "source": "Global Honeynet Network",
        "target_sector": "IoT & Edge Routers",
        "description": "Active botnet node scanning for open Telnet (port 23) and SSH credentials.",
        "recommended_action": "Ensure perimeter devices have default credentials modified and administrative ports isolated from public Internet.",
        "status": "ACTIVE",
        "country_code": "BR",
    },
    {
        "ioc_value": "http://malicious-update-server.net/payload.exe",
        "ioc_type": "url",
        "threat_type": "Drive-by Download",
        "severity": "CRITICAL",
        "confidence_score": 96.0,
        "source": "SecureVision Threat Sensor",
        "target_sector": "E-Commerce Infrastructure",
        "description": "Active URL hosting infected executable payload disguised as browser update package.",
        "recommended_action": "Block URL string on Secure Web Gateway (SWG) and notify incident response team.",
        "status": "ACTIVE",
        "country_code": "NL",
    },
    {
        "ioc_value": "cve-2023-4863",
        "ioc_type": "cve",
        "threat_type": "Zero-Day Exploit",
        "severity": "HIGH",
        "confidence_score": 95.0,
        "source": "Google Threat Analysis Group",
        "target_sector": "Web Browsers & Electron Apps",
        "description": "Heap buffer overflow in libwebp library leading to arbitrary code execution during image rendering.",
        "recommended_action": "Patch libwebp and update Chromium-based web browsers and desktop client frameworks immediately.",
        "status": "MITIGATED",
        "country_code": "US",
    },
    {
        "ioc_value": "45.142.214.19",
        "ioc_type": "ip",
        "threat_type": "DDoS Amplification Vector",
        "severity": "MEDIUM",
        "confidence_score": 81.0,
        "source": "Shodan Threat Scanner",
        "target_sector": "Telecommunications",
        "description": "Misconfigured NTP server utilized in high-volume UDP reflection amplification attacks.",
        "recommended_action": "Rate-limit UDP NTP response packets and restrict monlist command responses.",
        "status": "INVESTIGATING",
        "country_code": "FR",
    }
]

class ThreatIntelRepository(BaseRepository[ThreatIOC]):
    def __init__(self):
        super().__init__(ThreatIOC)

    def seed_initial_iocs(self, db: Session) -> None:
        """Seed baseline IOC threat feed data if table is currently empty."""
        count = db.query(self.model).count()
        if count == 0:
            for item in SEED_THREAT_DATA:
                ioc = ThreatIOC(**item)
                db.add(ioc)
            db.commit()

    def get_feed(
        self,
        db: Session,
        limit: int = 50,
        severity: Optional[str] = None,
        ioc_type: Optional[str] = None,
        search_query: Optional[str] = None,
    ) -> List[ThreatIOC]:
        query = db.query(self.model)

        if severity and severity.upper() != "ALL":
            query = query.filter(self.model.severity == severity.upper())

        if ioc_type and ioc_type.lower() != "all":
            query = query.filter(self.model.ioc_type == ioc_type.lower())

        if search_query and search_query.strip():
            sq = f"%{search_query.strip()}%"
            query = query.filter(
                (self.model.ioc_value.ilike(sq)) |
                (self.model.threat_type.ilike(sq)) |
                (self.model.source.ilike(sq)) |
                (self.model.target_sector.ilike(sq))
            )

        return query.order_by(self.model.created_at.desc()).limit(limit).all()

    def lookup_ioc(self, db: Session, query_str: str) -> Optional[ThreatIOC]:
        clean_query = query_str.strip().lower()
        return (
            db.query(self.model)
            .filter(func.lower(self.model.ioc_value) == clean_query)
            .first()
        )

    def get_stats(self, db: Session) -> dict:
        total = db.query(self.model).count()
        critical = db.query(self.model).filter(self.model.severity == "CRITICAL").count()
        high = db.query(self.model).filter(self.model.severity == "HIGH").count()
        medium = db.query(self.model).filter(self.model.severity == "MEDIUM").count()
        low = db.query(self.model).filter(self.model.severity == "LOW").count()

        # Calculate average confidence score
        avg_conf = db.query(func.avg(self.model.confidence_score)).scalar() or 90.0

        # Category distribution
        type_counts = (
            db.query(self.model.threat_type, func.count(self.model.id))
            .group_by(self.model.threat_type)
            .all()
        )
        category_distribution = {t: c for t, c in type_counts}

        top_vector = "Ransomware & C2 Infrastructure"
        if type_counts:
            sorted_types = sorted(type_counts, key=lambda x: x[1], reverse=True)
            top_vector = sorted_types[0][0]

        return {
            "total_active_iocs": total,
            "critical_threats": critical,
            "high_threats": high,
            "medium_threats": medium,
            "low_threats": low,
            "top_threat_vector": top_vector,
            "avg_confidence_score": round(float(avg_conf), 1),
            "category_distribution": category_distribution,
        }

threat_intel_repository = ThreatIntelRepository()
