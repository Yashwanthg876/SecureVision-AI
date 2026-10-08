import httpx # type: ignore
from bs4 import BeautifulSoup # type: ignore
from app.schemas.website_security import TechnologyInfo

async def analyze_technology(url: str) -> TechnologyInfo:
    """
    Identifies the underlying technology stack using HTTP response headers and HTML meta tags.
    """
    server = None
    x_powered_by = None
    frameworks = set()
    
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=False) as client:
            server = None
            x_powered_by = None
            body_chunks = []
            total_size = 0
            max_size = 512 * 1024  # 512 KB limit to prevent OOM
            
            async with client.stream("GET", url) as response:
                headers = response.headers
                
                # 1. Header Analysis
                server = headers.get("server")
                x_powered_by = headers.get("x-powered-by")
                
                if x_powered_by:
                    frameworks.add(x_powered_by.split("/")[0])
                    
                if headers.get("x-aspnet-version"):
                    frameworks.add("ASP.NET")
                    
                async for chunk in response.aiter_bytes():
                    body_chunks.append(chunk)
                    total_size += len(chunk)
                    if total_size >= max_size:
                        break

            # 2. HTML Meta Analysis
            html_text = b"".join(body_chunks).decode("utf-8", errors="ignore")
            soup = BeautifulSoup(html_text, "html.parser")
            generator = soup.find("meta", attrs={"name": "generator"})
            if generator and generator.get("content"):
                frameworks.add(generator["content"].split(" ")[0])
                
            # Detect common frameworks from scripts/links
            scripts = [s.get("src", "") for s in soup.find_all("script") if s.get("src")]
            for script in scripts:
                script = script.lower()
                if "wp-content" in script or "wp-includes" in script:
                    frameworks.add("WordPress")
                if "next" in script or "_next" in script:
                    frameworks.add("Next.js")
                if "nuxt" in script or "_nuxt" in script:
                    frameworks.add("Nuxt.js")
                if "react" in script:
                    frameworks.add("React")
                if "vue" in script:
                    frameworks.add("Vue.js")
                if "angular" in script:
                    frameworks.add("Angular")
                    
            return TechnologyInfo(
                server=server,
                x_powered_by=x_powered_by,
                frameworks=list(frameworks)
            )
    except Exception:
        return TechnologyInfo(
            server=None,
            x_powered_by=None,
            frameworks=[]
        )
