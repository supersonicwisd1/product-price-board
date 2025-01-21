# app/models/suggestion.py

from sqlalchemy import Column, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.product import Product

class Suggestion(Base):
    __tablename__ = "suggestions"
    
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    suggested_price = Column(Float, nullable=False)
    username = Column(String, nullable=False)

    product = relationship("Product", back_populates="suggestions")
