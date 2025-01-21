# app/core/tasks.py

from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.price_calculator import PriceCalculatorService
from app.db.session import SessionLocal
from app.models.product import Product

# Function that performs the price update
price_calculator_service = PriceCalculatorService(db=None)
def update_prices_every_two_weeks():
    db = SessionLocal()
    try:
        two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
        products_to_update = db.query(Product).filter(Product.last_suggested >= two_weeks_ago).all()

        for product in products_to_update:
            new_price = price_calculator_service.calculate_new_price(db, product.id)  # pass db session and product ID
            if new_price:
                product.price = new_price
                db.add(product)
        
        db.commit()
        print("Prices updated successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error updating prices: {e}")
    finally:
        db.close()

# Start APScheduler to run the update task
def start_scheduler():
    scheduler = BackgroundScheduler()
    # This will run every 14 days (2 weeks)
    scheduler.add_job(update_prices_every_two_weeks, 'interval', weeks=2)
    scheduler.start()
