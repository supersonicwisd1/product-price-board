# app/api/__init__.py

from fastapi import APIRouter
from app.api.routes import auth, products, categories, reviews, suggestions, health

api_router = APIRouter()

# Include all route modules
api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(categories.router, prefix="/categories", tags=["Categories"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(suggestions.router, prefix="/suggestions", tags=["Suggestions"])
api_router.include_router(health.router, tags=["Health"])
