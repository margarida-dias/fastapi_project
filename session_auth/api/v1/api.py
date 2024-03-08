from fastapi import APIRouter

from session_auth.api.v1.endpoints import product
from session_auth.api.v1.endpoints import user

api_router = APIRouter()
api_router.include_router(product.router, prefix='/products', tags=["products"])
api_router.include_router(user.router, prefix='/users', tags=["users"])