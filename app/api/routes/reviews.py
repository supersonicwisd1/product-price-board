# app/api/routes/reviews.py

from fastapi import APIRouter, Depends, HTTPException, status
from app.crud.review import crud_review
from app.schemas.review import ReviewCreate, ReviewRead
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=ReviewCreate)
def create_review(review_in: ReviewCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions"
        )
    review_in.user_id = current_user.id 
    return crud_review.create(db, review_in)


@router.get("/{product_id}", response_model=list[ReviewRead])
def get_reviews_for_product(product_id: int, db: Session = Depends(get_db)):
    return crud_review.get_by_product(db, product_id)
