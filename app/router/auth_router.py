from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, database, utils, oauth2, schemas


authapi = APIRouter(tags=["Authentication"])

@authapi.post("/login", response_model=schemas.Token)
async def login(user_cred:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)): 
    log_user = db.query(models.Users).filter(models.Users.email == user_cred.username).first()
    
    if not log_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.pass_verifier(user_cred.password, log_user.password): 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id":log_user.id})

    return {"Authorization":"Success","access_token":access_token, "token_type":"bearer"}