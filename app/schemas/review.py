# app/schemas/review.py

from pydantic import BaseModel
from typing import Optional
from app.schemas.user import UserPublic
# from app.schemas.product import ProductRead

class ReviewBase(BaseModel):
    price: float
    market: str
    extra_note: Optional[str] = None

class ReviewCreate(ReviewBase):
    product_id: int

class ReviewUpdate(ReviewBase):
    user_id: int
    product_id: int

class ReviewRead(ReviewBase):
    id: int
    user: Optional[UserPublic]
    # product: ProductRead

    class Config:
        from_attributes = True
