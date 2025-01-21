# app/crud/category.py

from sqlalchemy.orm import Session
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate

class CRUDCategory:
    def create(self, db: Session, category_in: CategoryCreate) -> Category:
        category = Category(**category_in.dict())
        db.add(category)
        db.commit()
        db.refresh(category)
        return category

    def get(self, db: Session, category_id: int) -> Category | None:
        return db.query(Category).filter(Category.id == category_id).first()

    def get_all(self, db: Session, skip: int = 0, limit: int = 10) -> list[Category]:
        return db.query(Category).offset(skip).limit(limit).all()

    def update(self, db: Session, category: Category, category_in: CategoryUpdate) -> Category:
        for field, value in category_in.dict(exclude_unset=True).items():
            setattr(category, field, value)
        db.commit()
        db.refresh(category)
        return category

    def delete(self, db: Session, category: Category) -> None:
        db.delete(category)
        db.commit()

crud_category = CRUDCategory()
