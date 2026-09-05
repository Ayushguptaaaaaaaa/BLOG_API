from jose import jwt,JWTError
from datetime import datetime,timedelta,timezone
from fastapi import HTTPException,Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

#token create
def create_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(timezone.utc)+ timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)


def verify_token(token: str = Depends(oauth2_schema)):
    if token is None:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload is None:
            raise HTTPException(status_code=401, detail="Invalid Token")
        return payload
    except JWTError as e:
        raise HTTPException(status_code=401, detail="Invalid Token")