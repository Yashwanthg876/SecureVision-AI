from app.schemas.website_security import (
    SSLInfo, HTTPHeadersInfo, DNSInfo, WHOISInfo, TechnologyInfo, Recommendation
)
from typing import List

def generate_recommendations(
    ssl_info: SSLInfo,
    headers_info: HTTPHeadersInfo,
    dns_info: DNSInfo,
    whois_info: WHOISInfo,
    tech_info: TechnologyInfo
) -> List[Recommendation]:
    """
    Analyzes all aggregated data to generate a deterministic list of actionable recommendations.
    """
    recommendations = []
    
    # SSL Recommendations
    if not ssl_info.is_valid:
        recommendations.append(Recommendation(
            category="SSL",
            title="Invalid or Missing SSL/TLS Certificate",
            description="No valid SSL/TLS certificate was detected. This means traffic between the client and server is unencrypted or the certificate chain is untrusted.",
            severity="Critical",
            recommendation="Provision and install a valid SSL/TLS certificate from a trusted Certificate Authority (e.g., Let's Encrypt).",
            reference="https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"
        ))
    elif ssl_info.expires_in_days is not None and ssl_info.expires_in_days < 30:
        recommendations.append(Recommendation(
            category="SSL",
            title=f"SSL/TLS Certificate expiring in {ssl_info.expires_in_days} days",
            description="The SSL certificate is nearing its expiration date. Once expired, browsers will show a security warning to users.",
            severity="High",
            recommendation="Renew the SSL certificate immediately to prevent service disruption and security warnings.",
            reference="https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Protection_Cheat_Sheet.html"
        ))

    # Header Recommendations
    if not headers_info.strict_transport_security:
        recommendations.append(Recommendation(
            category="Headers",
            title="Missing Strict-Transport-Security (HSTS) Header",
            description="The HTTP Strict-Transport-Security response header is missing. This allows potential man-in-the-middle attacks to downgrade connections to HTTP.",
            severity="High",
            recommendation="Configure the web server to enforce HSTS by adding the 'Strict-Transport-Security: max-age=31536000; includeSubDomains' header.",
            reference="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security"
        ))
    if not headers_info.content_security_policy:
        recommendations.append(Recommendation(
            category="Headers",
            title="Missing Content-Security-Policy (CSP) Header",
            description="No Content Security Policy detected. A CSP helps detect and mitigate certain types of attacks, including Cross-Site Scripting (XSS) and data injection.",
            severity="Medium",
            recommendation="Implement a strong CSP using the 'Content-Security-Policy' header to restrict the resources that the browser is allowed to load.",
            reference="https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP"
        ))
    if not headers_info.x_frame_options:
        recommendations.append(Recommendation(
            category="Headers",
            title="Missing X-Frame-Options Header",
            description="The site does not prevent clickjacking attacks via the X-Frame-Options header.",
            severity="Low",
            recommendation="Add 'X-Frame-Options: DENY' or 'SAMEORIGIN' to prevent the page from being embedded in an iframe.",
            reference="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"
        ))
    if not headers_info.x_content_type_options:
        recommendations.append(Recommendation(
            category="Headers",
            title="Missing X-Content-Type-Options Header",
            description="The site is missing MIME-sniffing protection.",
            severity="Low",
            recommendation="Add 'X-Content-Type-Options: nosniff' to prevent MIME-sniffing vulnerabilities.",
            reference="https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Content-Type-Options"
        ))

    # DNS Recommendations
    if not dns_info.has_spf:
        recommendations.append(Recommendation(
            category="DNS",
            title="Missing SPF Record",
            description="Sender Policy Framework (SPF) records are missing. Attackers could spoof emails appearing to come from this domain.",
            severity="Medium",
            recommendation="Publish an SPF record in DNS to specify which mail servers are authorized to send email on behalf of your domain.",
            reference="https://www.cloudflare.com/learning/dns/dns-records/dns-spf-record/"
        ))
    if not dns_info.has_dmarc:
        recommendations.append(Recommendation(
            category="DNS",
            title="Missing DMARC Record",
            description="DMARC records are missing, leaving the domain vulnerable to email spoofing and phishing.",
            severity="Medium",
            recommendation="Implement a DMARC policy to protect your domain from unauthorized use.",
            reference="https://dmarc.org/overview/"
        ))

    # Tech Stack Recommendations
    if tech_info.server or tech_info.x_powered_by:
        recommendations.append(Recommendation(
            category="Tech",
            title="Information Disclosure via HTTP Headers",
            description="The server leaks infrastructure information via the 'Server' or 'X-Powered-By' headers.",
            severity="Low",
            recommendation="Remove or obfuscate 'Server' and 'X-Powered-By' headers to prevent attackers from footprinting your technology stack.",
            reference="https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/01-Information_Gathering/02-Fingerprint_Web_Server"
        ))
        
    return recommendations
