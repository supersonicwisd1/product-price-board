# app/models/review.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.product import Product
from app.models.user import User

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    market = Column(String, nullable=False)
    extra_note = Column(String, nullable=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    user = relationship("User", back_populates="reviews")
    product = relationship("Product", back_populates="reviews")
