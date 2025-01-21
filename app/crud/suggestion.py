# app/crud/suggestion.py

from sqlalchemy.orm import Session
from app.models.suggestion import Suggestion
from app.schemas.suggestion import SuggestionCreate

class CRUDSuggestion:
    def create(self, db: Session, suggestion_in: SuggestionCreate) -> Suggestion:
        suggestion = Suggestion(**suggestion_in.dict())
        db.add(suggestion)
        db.commit()
        db.refresh(suggestion)
        return suggestion

    def get_by_product(self, db: Session, product_id: int) -> list[Suggestion]:
        return db.query(Suggestion).filter(Suggestion.product_id == product_id).all()

crud_suggestion = CRUDSuggestion()
