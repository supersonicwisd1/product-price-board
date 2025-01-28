# app/api/routes/products.py

from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from app.crud.product import crud_product
from app.schemas.product import ProductCreate, ProductUpdate, ProductRead
from app.schemas.review import ReviewRead, ReviewCreate
from app.api.dependencies import get_db
from app.models.user import User
from app.models.review import Review
from app.models.product import Product
from sqlalchemy.orm import Session
from app.core.security import get_current_user
import shutil
import os
from typing import Optional
from datetime import datetime

router = APIRouter()

UPLOAD_DIR = "uploads/"  # Directory to store uploaded files
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=ProductRead)
def create_product(
    name: str,
    price: float,
    category_id: int,
    image: Optional[UploadFile] = File(None),  # Default to None
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions"
        )

    file_path = None
    if image and image.filename:  # Ensure image is provided and has a valid filename
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    # Create product
    product_in = ProductCreate(name=name, price=price, category_id=category_id)
    product = crud_product.create(db, product_in)
    if file_path:
        product.image_url = file_path  # Save the file path if an image was uploaded
    db.commit()
    db.refresh(product)

    return product

@router.get("/", response_model=list[ProductCreate])
def get_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_product.get_all(db, skip=skip, limit=limit)

@router.get("/{product_id}", response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Eagerly load reviews
    product.reviews = crud_product.get_reviews(db, product_id)
    return product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product_id: int,
    name: str = None,
    price: float = None,
    category_id: int = None,
    image: Optional[UploadFile] = File(None),  # Optional file upload
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Retrieve the product
    product = crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )

    # Update fields selectively
    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if category_id is not None:
        product.category_id = category_id

    # Handle image upload
    if image:
        if image.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=400,
                detail="Only JPEG and PNG file types are allowed.",
            )
        file_path = os.path.join(UPLOAD_DIR, image.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        product.image_url = file_path  # Update the file path in the database

    db.commit()
    db.refresh(product)

    return product

@router.delete("/{product_id}", response_model=ProductCreate)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = crud_product.get(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")
    crud_product.delete(db, product)
    return {"message": "Product deleted"}

@router.post("/{product_id}/reviews", response_model=ReviewRead)
def create_review(
    product_id: int, 
    review: ReviewCreate, 
    db: Session = Depends(get_db), 
    user: User = Depends(get_current_user)  # Ensure logged-in user
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found."
        )
    
    # Create a new review linked to the current user
    new_review = Review(
        price=review.price,
        market=review.market,
        extra_note=review.extra_note,
        user_id=user.id,  # Associate the review with the logged-in user
        product_id=product_id,
    )
    db.add(new_review)

    # Update last_suggested field
    product.last_suggested = datetime.utcnow()
    db.add(product)

    db.commit()
    db.refresh(new_review)

    return new_review
    return new_review

# @router.post("/{product_id}/reviews", response_model=ReviewRead)
# def create_review(
#     product_id: int,
#     review: ReviewCreate,  # Review input without product_id
#     db: Session = Depends(get_db),
#     user: User = Depends(get_current_user),  # Ensure logged-in user
# ):
#     # Ensure the product exists
#     product = db.query(Product).filter(Product.id == product_id).first()
#     if not product:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Product with ID {product_id} not found."
#         )

#     # Optional: Check if the user has already reviewed the product
#     existing_review = (
#         db.query(Review)
#         .filter(Review.product_id == product_id, Review.user_id == user.id)
#         .first()
#     )
#     if existing_review:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="You have already reviewed this product."
#         )

#     # Create a new review linked to the current user and product
#     new_review = Review(
#         price=review.price,
#         market=review.market,
#         extra_note=review.extra_note,
#         user_id=user.id,
#         product_id=product_id,  # Use the product_id from the URL
#     )
#     db.add(new_review)
#     db.commit()
#     db.refresh(new_review)

#     return new_review
