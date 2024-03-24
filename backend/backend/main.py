from fastapi import FastAPI

from backend.routers import search
from backend.internal import db

app = FastAPI()
app.include_router(search.router, prefix='/search')

@app.get('/')
async def root():
    return {'message': 'PReview'}

@app.get('/reset')
async def reset(confirm: bool):
    if confirm:
        db.articles.delete_many({})