from googleapiclient.discovery import build
from scrapingbee import ScrapingBeeClient
from newspaper import Article
from dateutil.parser import parse as date_parse

from backend.internal import secrets
from backend.internal.models import ArticleModel

client = ScrapingBeeClient(secrets.SCRAPINGBEE_API_KEY)
service = build('customsearch', 'v1', developerKey=secrets.GOOGLE_API_KEY)

def fetch_urls(query: str, cx=secrets.GOOGLE_CX) -> list[str]:
    response =  service.cse().list(
        q=query, 
        cx=cx, 
        sort='date',
    ).execute()

    return [item['link'] for item in response['items']]

def fetch_htmls(urls: list[str]) -> list[str]:
    htmls = []
    for url in urls:
        res = client.get(url)

        if res.status_code == 200:
            htmls.append(res.text)
    
    return htmls

def parse_articles(htmls: list[str]) -> list[ArticleModel]:
    art = Article('')

    articles = []
    for html in htmls:
        art.set_html(html)
        art.parse()

        articles.append(
            ArticleModel(
                title=art.title,
                source=art.meta_data['og']['site_name'],
                url=art.meta_data['og']['url'],
                authors=art.authors,
                # published=date_parse(art.meta_data['article']['published']),
                text=art.text
            )
        )
    
    return articles

def scrape_articles(query: str) -> list[ArticleModel]:
    urls = fetch_urls(query)
    htmls = fetch_htmls(urls)
    return parse_articles(htmls)