# app/api/routes/suggestions.py

from fastapi import APIRouter, Depends, HTTPException
from app.crud.suggestion import crud_suggestion
from app.schemas.suggestion import SuggestionCreate, SuggestionRead
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=SuggestionCreate)
def create_suggestion(suggestion_in: SuggestionCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")
    return crud_suggestion.create(db, suggestion_in)

@router.get("/{product_id}", response_model=list[SuggestionRead])
def get_suggestions_for_product(product_id: int, db: Session = Depends(get_db)):
    return crud_suggestion.get_by_product(db, product_id)
