from fastapi import APIRouter, HTTPException

from backend.internal.scrape import scrape_articles
from backend.internal import db

router = APIRouter()

@router.post('/{query}')
async def execute(query: str, page:int):
    articles = [
        a.model_dump(by_alias=True, exclude=['id']) 
        for a in scrape_articles(query, page)
    ]
    inserts = await db.articles.insert_many(articles)

    return [str(i) for i in inserts.inserted_ids]
