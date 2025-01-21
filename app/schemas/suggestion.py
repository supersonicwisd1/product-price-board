# app/schemas/suggestion.py

from pydantic import BaseModel

class SuggestionBase(BaseModel):
    product_id: int
    suggested_price: float

class SuggestionCreate(SuggestionBase):
    username: str

class SuggestionRead(SuggestionBase):
    id: int
    username: str

    class Config:
        from_attributes = True
