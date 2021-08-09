from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from . import schemas


SECRET_KEY = "f9e5da3427cfac7b45532d349a2752026fb8fd052cb7461f63680c6a298234ad"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        password: str = payload["sub"]
        if password is None:
            raise credentials_exception
        token_data = schemas.TokenData(password=password)
    except JWTError:
        return {"success": False, "message": "invalid token"}
