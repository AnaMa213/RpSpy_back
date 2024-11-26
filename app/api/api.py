from fastapi import APIRouter

from app.api.endpoints import user_controller as users

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
