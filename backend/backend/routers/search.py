from fastapi import APIRouter, HTTPException

from backend.internal import scrape

router = APIRouter()

@router.get('/{query}')
async def execute(query: str, type: str):
    pass