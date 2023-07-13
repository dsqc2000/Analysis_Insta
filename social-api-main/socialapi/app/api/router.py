from fastapi import APIRouter


from api.endpoints.post_endpoints import router as post_router



router = APIRouter()




router.include_router(post_router, prefix="/posts", tags=["Posts"])