from sqlalchemy.orm import Session
from app.models.review import Review

class ReviewAnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def analyze_reviews(self, product_id: int) -> dict:
        reviews = self.db.query(Review).filter(Review.product_id == product_id).all()

        if not reviews:
            return {"average_rating": 0, "notes": []}

        average_price = sum(r.price for r in reviews) / len(reviews)
        notes = [r.extra_note for r in reviews if r.extra_note]
        
        return {
            "average_rating": average_price,
            "notes": notes
        }

    def analyze_reviews_background(self, background_tasks, product_id: int) -> None:
        """
        Add background task for review analysis.
        """
        background_tasks.add_task(self.analyze_reviews, product_id)
