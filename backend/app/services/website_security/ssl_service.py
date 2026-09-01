import ssl
import socket
from datetime import datetime, timezone
from app.schemas.website_security import SSLInfo

def analyze_ssl(hostname: str) -> SSLInfo:
    """
    Connects to the host on port 443 to retrieve and analyze the SSL certificate.
    """
    try:
        # First try standard context with cert dictionary extraction
        context = ssl.create_default_context()
        protocol = "TLS"
        cert_dict = None
        is_valid = True

        try:
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert_dict = ssock.getpeercert()
                    protocol = ssock.version() or "TLS"
        except Exception:
            # If verification failed (e.g. self-signed or expired), connect without verify to inspect certificate
            is_valid = False
            unverified_context = ssl.create_default_context()
            unverified_context.check_hostname = False
            unverified_context.verify_mode = ssl.CERT_NONE

            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with unverified_context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    protocol = ssock.version() or "TLS"

        if cert_dict:
            not_after_str = cert_dict.get('notAfter')
            if not_after_str:
                not_after = ssl.cert_time_to_seconds(not_after_str)
                expires_in = (datetime.fromtimestamp(not_after, tz=timezone.utc) - datetime.now(timezone.utc)).days
            else:
                expires_in = 0

            issuer = dict(x[0] for x in cert_dict.get('issuer', []))
            subject = dict(x[0] for x in cert_dict.get('subject', []))

            issuer_name = issuer.get('organizationName', issuer.get('commonName', 'Unknown'))
            subject_name = subject.get('commonName', 'Unknown')
        else:
            issuer_name = "Self-Signed / Untrusted Issuer"
            subject_name = hostname
            expires_in = 0

        return SSLInfo(
            is_valid=is_valid,
            issuer=issuer_name,
            subject=subject_name,
            expires_in_days=expires_in,
            protocol=protocol,
            error=None if is_valid else "SSL Certificate verification failed or cert untrusted"
        )
    except Exception as e:
        return SSLInfo(
            is_valid=False,
            issuer="Unknown",
            subject="Unknown",
            expires_in_days=0,
            protocol="Unknown",
            error=str(e)
        )
