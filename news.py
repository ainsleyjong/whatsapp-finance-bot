import requests
import time
import datetime as dt
from typing import Any
from config import (
    BASE_URL,
    API_KEY,
    DEFAULT_HOURS,
    REQUEST_TIMEOUT,
    SLEEP_BETWEEN_PAGES,
)

#---------- Helper Functions ----------#
def _utc_iso(hours_back: int) -> str:
    return (dt.datetime.now() - dt.timedelta(hours=hours_back)).replace(microsecond=0).isoformat()

def _hr(char: str = "-", width: int = 50) -> str: # Horizontal Rule
    return char * width

def _fetch_page(params: dict[str, Any]) -> dict[str, Any]:
    resp = requests.get(BASE_URL, params=params, timeout=REQUEST_TIMEOUT)
    if resp.status_code != 200:
        raise RuntimeError(f"Marketaux error {resp.status_code}: {resp.text[:500]}")
    return resp.json()

#--------------------------------------#

def extract_data(pages: int, 
                 symbols: str | None = None, 
                 industries: str | None = None
                 ) -> list[dict[str, Any]]:
    base_params = {
        "api_token": API_KEY,
        "language": "en",
        "published_after": _utc_iso(DEFAULT_HOURS),
        "must_have_entities": "true",
        "countries": "us,ca",
        "group_similar": "true",
        "limit": 3
    }
    if symbols:
        base_params["symbols"] = symbols
    if industries:
        base_params["industries"] = industries

    articles: list[dict[str, Any]] = []

    for page in range(1, pages + 1):
        params = dict(base_params, page=page)
        payload = _fetch_page(params)

        data = payload.get("data", [])
        if not data:
            break

        for a in data:
            article = {
                "title": a.get("title", "No Title"),
                "description": a.get("description", "No Description"),
                "url": a.get("url", "No URL"),
                "similar": [
                    {
                        "title": s.get("title", "No Title"),
                        "description": s.get("description", "No Description"),
                        "url": s.get("url", "No URL")
                    }
                    for s in a.get("similar", []) or []
                ]
            }
            articles.append(article)

        time.sleep(SLEEP_BETWEEN_PAGES)

    return articles

def print_articles(articles: list[dict], header: str):
    print(f"\n{header}")
    print(_hr())
    for i, a in enumerate(articles, start = 1):
        print(f"\n{i:02d}. {a["title"]}")
        print(f"    {a["description"]}")
        print(f"    URL: {a["url"]}")
        
        if a["similar"]:
            for j, s in enumerate(a["similar"], start=1):
                print(f"    ↳ Related {j}: {s["title"]}")
                print(f"                 {s["description"]}")
                print(f"                 {s["url"]}")


                