from passlib.context import CryptContext
from jose import jwt

from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "PASSWORDKEY123"
ALGORITHM = "HS256"
ACCESS_TOKEN_TIME = 60

def verify_pass(plainpassword: str , hashed_password: str):
    return pwd_context.verify(plainpassword, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_TIME)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt