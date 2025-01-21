# app/crud/review.py

from sqlalchemy.orm import Session, joinedload
from app.models.review import Review
from app.schemas.review import ReviewCreate, ReviewUpdate

class CRUDReview:
    def create(self, db: Session, review_in: ReviewCreate) -> Review:
        review = Review(**review_in.dict())
        db.add(review)
        db.commit()
        db.refresh(review)
        return review

    def get(self, db: Session, review_id: int) -> Review | None:
        return db.query(Review).filter(Review.id == review_id).first()

    def get_by_product(self, db: Session, product_id: int) -> list[Review]:
        return db.query(Review).options(joinedload(Review.user)).filter(Review.product_id == product_id).all()

    def update(self, db: Session, review: Review, review_in: ReviewUpdate) -> Review:
        for field, value in review_in.dict(exclude_unset=True).items():
            setattr(review, field, value)
        db.commit()
        db.refresh(review)
        return review

    def delete(self, db: Session, review: Review) -> None:
        db.delete(review)
        db.commit()

crud_review = CRUDReview()
