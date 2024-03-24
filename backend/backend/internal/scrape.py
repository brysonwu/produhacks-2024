from googleapiclient.discovery import build
from scrapingbee import ScrapingBeeClient

from backend.internal import secrets

client = ScrapingBeeClient(secrets.SCRAPINGBEE_API_KEY)
service = build('customsearch', 'v1', developerKey=secrets.GOOGLE_API_KEY)

def google_search(query: str, cx=secrets.GOOGLE_CX):
    return service.cse().list(q=query, cx=cx).execute()

def fetch_htmls(urls: list[str]):
    htmls = []
    for url in urls:
        res = client.get(url)

        if res.status_code == 200:
            htmls.append(res.text)
    
    return htmls

def parse_articles(urls: list[str]):
    htmls = fetch_htmls(urls)
    for html in htmls:
        pass
