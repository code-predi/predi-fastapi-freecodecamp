from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import app.schemas as schemas
import app.database as database
import app.models as models
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

_SECRET_KEY = settings.secret_key
_ALGORITHM = settings.algorithm
_ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _SECRET_KEY, algorithm= _ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception): 
    try:
        payload = jwt.decode(token=token, key=_SECRET_KEY, algorithms=[_ALGORITHM])
        user_id : str = payload.get("user_id")
        if not user_id: 
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError: 
        raise credentials_exception
    return token_data

def get_current_token(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)): 
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail=f"Could not authorize user", headers={
                                "WWW-Authenticate":"Bearer"
                            })
    token_data = verify_access_token(token=token, credentials_exception=credentials_exception)
    user_data = db.query(models.Users).filter(models.Users.id == token_data.id).first()

    return user_data