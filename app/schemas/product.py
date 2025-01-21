# app/schemas/product.py

from pydantic import BaseModel, field_validator
from typing import Optional, List
from app.schemas.review import ReviewRead
from app.utils.image_utils import get_file_url

class ProductBase(BaseModel):
    name: str
    price: float
    image_url: Optional[str] = None

class ProductCreate(ProductBase):
    category_id: int

class ProductRead(ProductBase):
    id: int
    category_id: int
    image_url: Optional[str] = None
    reviews: List[ReviewRead] = []

    @field_validator('image_url')
    def transform_image_url(cls, v):
        if v:
            return get_file_url(v)
        return None

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

    @field_validator('image_url')
    def transform_image_url(cls, v):
        if v:
            return get_file_url(v)
        return None
