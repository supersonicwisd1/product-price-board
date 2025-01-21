# app/api/routes/categories.py

from fastapi import APIRouter, Depends, HTTPException
from app.crud.category import crud_category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryRead
from app.api.dependencies import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/", response_model=CategoryCreate)
def create_category(category_in: CategoryCreate, db: Session = Depends(get_db)):
    return crud_category.create(db, category_in)

@router.get("/", response_model=list[CategoryRead])
def get_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_category.get_all(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud_category.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=CategoryUpdate)
def update_category(category_id: int, category_in: CategoryUpdate, db: Session = Depends(get_db)):
    category = crud_category.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud_category.update(db, category, category_in)

@router.delete("/{category_id}", response_model=CategoryCreate)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud_category.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    crud_category.delete(db, category)
    return {"message": "Category deleted"}
