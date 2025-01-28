# product_price_board/app/services/price_calculator.py
from sqlalchemy.orm import Session
from app.models.review import Review
from app.models.product import Product

class PriceCalculatorService:
    def __init__(self, db: Session):
        self.db = db

    def calculate_new_price(self, product_id: int, threshold: int = 5, price_tolerance: float = 0.5) -> float | None:
        """
        Calculate a new price for a product based on reviews while filtering out prices
        that deviate too far from the product's current price.

        Args:
            product_id (int): ID of the product.
            threshold (int): Minimum number of reviews required to calculate a new price.
            price_tolerance (float): Maximum allowable percentage deviation from the product's price (e.g., 0.5 for 50%).

        Returns:
            float | None: The new calculated price, or None if insufficient reviews or no valid product.
        """
        suggestions = self.db.query(Review).filter(Review.product_id == product_id).all()
        
        if len(suggestions) < threshold:
            return None  # Not enough suggestions to recalculate price

        # Fetch the current product price
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return None  # Product not found

        product_price = product.price
        suggested_prices = [s.price for s in suggestions]
        
        # Filter prices within the acceptable tolerance range
        filtered_prices = [
            price for price in suggested_prices
            if product_price * (1 - price_tolerance) <= price <= product_price * (1 + price_tolerance)
        ]
        
        if not filtered_prices:
            return None  # No prices within the tolerance range

        # Calculate the mean of the filtered prices and average it with the current product price
        mean_price = sum(filtered_prices) / len(filtered_prices)
        new_price = (mean_price + product_price) / 2
        
        return round(new_price, 2)


    def calculate_new_price_background(self, background_tasks, product_id: int, threshold: int = 5) -> None:
        """
        Add background task for price calculation.
        """
        background_tasks.add_task(self.calculate_new_price, product_id, threshold)
