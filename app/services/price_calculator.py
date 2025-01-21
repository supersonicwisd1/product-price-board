from sqlalchemy.orm import Session
from app.models.suggestion import Suggestion
from app.models.product import Product

class PriceCalculatorService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_new_price(self, product_id: int, threshold: int = 5) -> float | None:
        suggestions = self.db.query(Suggestion).filter(Suggestion.product_id == product_id).all()
        
        if len(suggestions) < threshold:
            return None  # Not enough suggestions to recalculate price

        suggested_prices = [s.suggested_price for s in suggestions]
        product = self.db.query(Product).filter(Product.id == product_id).first()

        if product:
            mean_price = sum(suggested_prices) / len(suggested_prices)
            new_price = (mean_price + product.price) / 2
            return round(new_price, 2)
        
        return None

    def calculate_new_price_background(self, background_tasks, product_id: int, threshold: int = 5) -> None:
        """
        Add background task for price calculation.
        """
        background_tasks.add_task(self.calculate_new_price, product_id, threshold)
