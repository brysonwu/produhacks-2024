from fastapi import APIRouter, HTTPException

from backend.internal.scrape import scrape_articles
from backend.internal import db

router = APIRouter()

@router.post('/{query}')
async def execute(query: str):
    articles = [
        a.model_dump(by_alias=True, exclude=['id']) 
        for a in scrape_articles(query)
    ]
    inserts = await db.articles.insert_many(articles)

    return inserts.inserted_ids
