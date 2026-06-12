from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.oauth2 import create_access_token
from passlib.context import CryptContext

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(credentials:OAuth2PasswordRequestForm = Depends(), db:Session=Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email==credentials.username
    ).first()
    if not user :
        raise HTTPException(status_code=403, detail="Invalid credentials")
    if not pwd_context.verify(credentials.password,user.hashed_password):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    token = create_access_token(data={"sub":str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
     