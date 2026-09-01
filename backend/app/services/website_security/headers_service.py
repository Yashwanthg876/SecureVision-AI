import httpx
from app.schemas.website_security import HTTPHeadersInfo

async def analyze_headers(url: str) -> HTTPHeadersInfo:
    """
    Performs a HEAD request to analyze security headers.
    """
    try:
        # Redirects are disabled so a public URL cannot redirect the scanner into
        # an internal network (SSRF).
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
            response = await client.head(url)
            headers = response.headers
            
            hsts = 'strict-transport-security' in headers
            csp = 'content-security-policy' in headers
            x_frame = 'x-frame-options' in headers
            x_content_type = 'x-content-type-options' in headers
            
            missing = []
            if not hsts: missing.append('Strict-Transport-Security')
            if not csp: missing.append('Content-Security-Policy')
            if not x_frame: missing.append('X-Frame-Options')
            if not x_content_type: missing.append('X-Content-Type-Options')
            
            return HTTPHeadersInfo(
                strict_transport_security=hsts,
                content_security_policy=csp,
                x_frame_options=x_frame,
                x_content_type_options=x_content_type,
                missing_headers=missing
            )
    except Exception:
        # Fallback to empty if host is unreachable
        return HTTPHeadersInfo(
            strict_transport_security=False,
            content_security_policy=False,
            x_frame_options=False,
            x_content_type_options=False,
            missing_headers=['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']
        )
