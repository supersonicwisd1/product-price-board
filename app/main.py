# app/main.py

from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import auth_router, product_router, category_router, review_router, suggestion_router, health_router
from app.core.config import settings
from app.services.notification import NotificationService
from app.services.review_analysis import ReviewAnalysisService
from app.services.price_calculator import PriceCalculatorService
from app.db.session import engine
from app.db.base import Base
from app.core.tasks import start_scheduler
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from fastapi.openapi.utils import get_openapi

# Create the FastAPI app
app = FastAPI(title="Price Board App")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="This is my API with Bearer Token Authentication",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",  # Optional
        }
    }
    openapi_schema["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# CORS Middleware to allow all origins for testing purposes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for different routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(category_router, prefix="/categories", tags=["Categories"])
# app.include_router(review_router, prefix="/reviews", tags=["Reviews"])
# app.include_router(suggestion_router, prefix="/suggestions", tags=["Suggestions"])
app.include_router(health_router, prefix="/health", tags=["Health"])

@app.on_event("startup")
async def startup():
    # Create the database tables (if needed)
    Base.metadata.create_all(bind=engine)
    
    print("App is starting up...")
    start_scheduler()

@app.on_event("shutdown")
async def shutdown():
    print("App is shutting down...")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Price Board API!"}

@app.post("/send_notification/")
async def send_email(background_tasks: BackgroundTasks, email: str, subject: str, body: str):
    notification_service = NotificationService()
    notification_service.send_notification_background(background_tasks, email, subject, body)
    return {"message": "Notification will be sent."}

@app.post("/calculate_price/")
async def recalculate_price(
    product_id: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Initialize the PriceCalculatorService with the database session
    price_calculator_service = PriceCalculatorService(db)
    # Use the service to add the background task for price recalculation
    price_calculator_service.calculate_new_price_background(background_tasks, product_id)
    return {"message": "Price recalculation task added."}

@app.post("/analyze_reviews/")
async def analyze_product_reviews(
    product_id: int, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    # Initialize the ReviewAnalysisService with the database session
    review_analysis_service = ReviewAnalysisService(db)
    # Use the service to add the background task for review analysis
    review_analysis_service.analyze_reviews_background(background_tasks, product_id)
    return {"message": "Review analysis task added."}
