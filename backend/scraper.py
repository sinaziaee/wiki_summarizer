import requests
from typing import Dict, List
from bs4 import BeautifulSoup

WIKI_API = "https://en.wikipedia.org/w/api.php"
WIKI_PAGE = "https://en.wikipedia.org/wiki"

def error_handling(response: requests.Response):
    if response.status_code != 200:
        raise Exception(f"Status {response.status_code}: {response.text[:100]}")

def search(query: str, limit: int=1) -> List[Dict]:
    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit,
    }
    response = requests.get(WIKI_API, params, timeout=100)
    error_handling(response)
    hits = response.json()['query']['search']
    if not hits:
        raise Exception(f"No page found for '{query}.'")
    return hits

def fetch_html(title: str) -> str:
    formatted_title = title.replace(" ", "_")
    url = f"{WIKI_PAGE}/{formatted_title}"
    response = requests.get(url, timeout=10)
    error_handling(response)
    return response.text, url

def clean_paragraph(p) -> str:
    """Remove superscripts, edit links, etc., from <p> tags."""
    for sup in p.select("sup"):
        sup.decompose()
    return p.get_text(strip=True)

def parse(html: str) -> Dict[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find(id="firstHeading").get_text(strip=True)
    paragraphs = [clean_paragraph(p) for p in soup.select("div.mw-parser-output > p") if p.get_text(strip=True)]
    lead = paragraphs[0] if paragraphs else ""
    return {"title": title, "lead": lead, "content": "\n\n".join(paragraphs)}

def scrape(query: str) -> Dict[str, str]:
    hit = search(query, limit=1)[0]
    html, url = fetch_html(hit['title'])
    return parse(html), url

data, url = scrape("Convocation")



