from fastapi import APIRouter
from api.v1.routes.users import router as users_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="", tags=["Users"])