from fastapi import status, HTTPException, Depends, APIRouter
from app.utils import password_hasher
from sqlalchemy.orm import Session
import app.models as models
from app.database import get_db
from app.schemas import UserCreate, ResponseUser

userapi = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@userapi.post("/create", status_code=status.HTTP_201_CREATED, response_model=ResponseUser)
async def create_user(user:UserCreate, db: Session = Depends(get_db)):
    hashed_password = password_hasher(user.password)
    user.password = hashed_password
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@userapi.get("/details/{id}", status_code=status.HTTP_200_OK, response_model=ResponseUser)
async def get_user_details(id:int, db: Session = Depends(get_db)): 
    user_details = db.query(models.Users).filter(models.Users.id == id).first()
    if not user_details: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} not found", headers={
            "error":"404"
        })
    return user_details