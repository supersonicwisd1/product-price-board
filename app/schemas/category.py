# app/schemas/category.py

from pydantic import BaseModel
from typing import List, Optional
from app.schemas.product import ProductRead

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryRead(CategoryBase):
    id: int
    products: Optional[List[ProductRead]] = []

    class Config:
        from_attributes = True
