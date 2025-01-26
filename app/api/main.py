from fastapi import APIRouter
from app.api.routes.users import user_router
from app.api.routes.products import product_router

api_router = APIRouter()

api_router.include_router(user_router)
api_router.include_router(product_router)