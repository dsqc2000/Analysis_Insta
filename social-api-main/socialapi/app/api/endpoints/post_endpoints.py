from typing import Any, List

from fastapi import APIRouter, HTTPException, Body, Depends, Path

from services.post_service import posts_service

router = APIRouter()

@router.get("/", response_description="Posts retrieved")
async def get_posts():
    """
        Get all posts
    """
    try:
        posts = await posts_service.get_multi()
        if posts:
            return posts
        return posts
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    


@router.get("/", response_description="Sentiment report retrieved")
async def get_sentiment():
    return None # sentiment report