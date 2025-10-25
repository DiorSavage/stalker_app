from fastapi import APIRouter
from api.v1.routes.users import router as users_router
from api.v1.routes.posts import router as posts_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="", tags=["Users"])
api_router.include_router(posts_router, prefix="", tags=["Posts"])