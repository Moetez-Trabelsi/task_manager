from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from passlib.context import CryptContext


router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

@router.post("/", status_code=201, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    exiting_user = db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    if exiting_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = pwd_context.hash(user.password)

    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password
    )


    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user