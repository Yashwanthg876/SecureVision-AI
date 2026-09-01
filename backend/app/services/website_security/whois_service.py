import whois
from app.schemas.website_security import WHOISInfo
from datetime import datetime, timezone
import asyncio

async def analyze_whois(hostname: str) -> WHOISInfo:
    """
    Performs a WHOIS lookup to determine registrar and domain expiration.
    """
    loop = asyncio.get_running_loop()
    
    def fetch_whois():
        try:
            return whois.whois(hostname)
        except Exception:
            return None
            
    domain_info = await loop.run_in_executor(None, fetch_whois)
    
    if not domain_info:
        return WHOISInfo(
            registrar="Unknown",
            creation_date=None,
            expiration_date=None,
            days_until_expiration=None
        )
        
    try:
        registrar_value = getattr(domain_info, "registrar", None)
        registrar = registrar_value if isinstance(registrar_value, str) and registrar_value.strip() else "Unknown"

        def first_value(value):
            if isinstance(value, (list, tuple)):
                return next((item for item in value if item is not None), None)
            return value

        creation = first_value(getattr(domain_info, "creation_date", None))
        creation_date = creation.strftime("%Y-%m-%d") if isinstance(creation, datetime) else (str(creation) if creation else None)

        expiration = first_value(getattr(domain_info, "expiration_date", None))
        expiration_date = None
        days_until_expiration = None
        if isinstance(expiration, datetime):
            expiration_date = expiration.strftime("%Y-%m-%d")
            if expiration.tzinfo is None:
                now = datetime.now()
            else:
                now = datetime.now(timezone.utc).astimezone(expiration.tzinfo)
            days_until_expiration = (expiration - now).days
        elif expiration:
            expiration_date = str(expiration)
    except Exception:
        registrar = "Unknown"
        creation_date = None
        expiration_date = None
        days_until_expiration = None
            
    return WHOISInfo(
        registrar=registrar,
        creation_date=creation_date,
        expiration_date=expiration_date,
        days_until_expiration=days_until_expiration
    )
