import dns.resolver
from app.schemas.website_security import DNSInfo
import asyncio

async def analyze_dns(hostname: str) -> DNSInfo:
    """
    Performs DNS lookups for A, MX, and TXT records to determine SPF and DMARC existence.
    """
    a_records = []
    mx_records = []
    txt_records = []
    
    # Run synchronous DNS resolution in a thread pool to avoid blocking the event loop
    loop = asyncio.get_running_loop()
    
    def resolve_records():
        try:
            answers = dns.resolver.resolve(hostname, 'A')
            a_records.extend([rdata.to_text() for rdata in answers])
        except Exception:
            pass
            
        try:
            answers = dns.resolver.resolve(hostname, 'MX')
            mx_records.extend([rdata.to_text() for rdata in answers])
        except Exception:
            pass
            
        try:
            answers = dns.resolver.resolve(hostname, 'TXT')
            txt_records.extend([rdata.to_text() for rdata in answers])
        except Exception:
            pass
            
    await loop.run_in_executor(None, resolve_records)
    
    has_spf = any('v=spf1' in txt for txt in txt_records)
    
    # DMARC is usually on _dmarc.hostname
    has_dmarc = False
    def resolve_dmarc():
        try:
            answers = dns.resolver.resolve(f'_dmarc.{hostname}', 'TXT')
            for rdata in answers:
                if 'v=DMARC1' in rdata.to_text():
                    return True
        except Exception:
            pass
        return False
        
    has_dmarc = await loop.run_in_executor(None, resolve_dmarc)
    
    return DNSInfo(
        a_records=a_records,
        mx_records=mx_records,
        txt_records=txt_records,
        has_spf=has_spf,
        has_dmarc=has_dmarc
    )
