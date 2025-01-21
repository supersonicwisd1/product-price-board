# app/api/routes/auth.py

from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserLogin, UserRead, Token
from app.crud.user import crud_user
from app.core.security import verify_password, create_access_token, get_current_user, get_current_token, get_active_user
from app.api.dependencies import get_db
from sqlalchemy.orm import Session
from app.models.user import User

router = APIRouter()

@router.post("/signup", response_model=UserRead)
def sign_up(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_user = crud_user.get_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    return crud_user.create(db, user_in)

@router.post("/login")
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = crud_user.get_by_email(db, user_in.email)
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user_in.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    access_token = create_access_token(data={"sub": current_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/protected")
def protected_route(current_user: str = Depends(get_current_user)):
    return {"message": f"Hello, {current_user}!"}

@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/admin-only")
def admin_route(current_user: User = Depends(get_active_user)):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have the necessary permissions",
        )
    return {"message": "Welcome, Admin!"}

@router.post("/logout")
async def logout(
    current_user: UserRead = Depends(get_current_user),
    token: str = Depends(get_current_token),
    db: Session = Depends(get_db)
):
    try:
        # Add token to blacklist
        blacklist_entry = TokenBlacklist(
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=1)  # Or match your JWT expiry
        )
        db.add(blacklist_entry)
        db.commit()

        return {
            "status": "success",
            "message": "Successfully logged out",
            "user": current_user.username
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Logout failed: {str(e)}"
        )
