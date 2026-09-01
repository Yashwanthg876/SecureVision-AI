import ipaddress
import socket
import urllib.parse


def _is_public_address(address: str) -> bool:
    ip = ipaddress.ip_address(address)
    return ip.is_global

def validate_url(url: str) -> str:
    """
    Validates and sanitizes a URL for passive scanning.
    Ensures the URL has a scheme and returns the hostname.
    """
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Invalid URL provided")
    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not allowed")
    try:
        port = parsed.port
    except ValueError as exc:
        raise ValueError("Invalid URL port") from exc
    if port not in (None, 80, 443):
        raise ValueError("Only HTTP and HTTPS default ports are allowed")

    hostname = parsed.hostname.rstrip(".").lower()
    if hostname == "localhost" or hostname.endswith(".localhost"):
        raise ValueError("Local and private network targets are not allowed")
    try:
        addresses = {item[4][0] for item in socket.getaddrinfo(hostname, port or 443)}
    except socket.gaierror as exc:
        raise ValueError("Target hostname could not be resolved") from exc
    if not addresses or any(not _is_public_address(address) for address in addresses):
        raise ValueError("Local and private network targets are not allowed")

    netloc = hostname if port is None else f"{hostname}:{port}"
    clean_url = urllib.parse.urlunsplit((parsed.scheme, netloc, parsed.path or "/", parsed.query, ""))
    return hostname, clean_url
