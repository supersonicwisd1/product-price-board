# app/crud/product.py

from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.review import Review

class CRUDProduct:
    def create(self, db: Session, product_in: ProductCreate) -> Product:
        product = Product(**product_in.dict())
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def get(self, db: Session, product_id: int) -> Product | None:
        return db.query(Product).options(joinedload(Product.reviews).joinedload(Review.user)).filter(Product.id == product_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> list[Product]:
        return db.query(Product).offset(skip).limit(limit).all()

    def update(self, db: Session, db_obj: Product, obj_in: dict):
        for field, value in obj_in.items():
            setattr(db_obj, field, value)  # Update only provided fields
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, product: Product) -> None:
        db.delete(product)
        db.commit()

    def get_reviews(self, db: Session, product_id: int):
        return db.query(Review).options(joinedload(Review.user)).filter(Review.product_id == product_id).all()


crud_product = CRUDProduct()
