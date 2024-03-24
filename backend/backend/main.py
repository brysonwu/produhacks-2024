from fastapi import FastAPI

from backend.routers import search

app = FastAPI()
app.include_router(search.router, prefix='/search')

@app.get('/')
async def root():
    return {'message': 'PReview'}