from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt

from db.models.user import User
from db.db_setup import get_db
from pydantic_schemas.user import UserCreate
from .utils.login import verify_pass, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)


@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered.")
    
    hashed_password = hash_password(user.password)
    new_user = User(email = user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"messgae" : "User Registered.", "user": {"id" :new_user.id, "email": new_user.email}}


@router.post("/login")
async def login(user: UserCreate, db:Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Email Doesn't Exist.")
    if not verify_pass(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid Password")
    
    access_token = create_access_token(data={"sub": str(db_user.id)})
    return{"access_token" : access_token, "token_type": "bearer"}