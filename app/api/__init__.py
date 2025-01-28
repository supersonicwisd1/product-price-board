# app/api/__init__.py

from fastapi import APIRouter
from app.api.routes import auth, products, categories,health

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(health.router, tags=["Health"])
