from pydantic import BaseModel, EmailStr, ConfigDict, conint
from datetime import datetime
from typing import Optional



#------------USER Schemas-------------#
class UserCreate(BaseModel): 
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ResponseUser(BaseModel):
    id: int 
    email: str
    created_at: datetime

    class Config: 
        orm_mode: True


#------------POST Schemas-------------#
        

class PostsBase(BaseModel): 
    title: str 
    content: str
    published: bool = True

class PostCreate(PostsBase): 
    pass

class PostUpdate(PostsBase):
    pass

class ResponsePost(PostsBase):
    id: int 
    created_at: datetime
    owner_info : ResponseUser
    owner_id :int 
    class Config: 
        orm_mode:True




#------------TOKEN Schemas-------------#
        
class Token(BaseModel): 
    access_token : str
    token_type : str

class TokenData(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True) 
    id : str


#-----------VOTE Schemas---------------#
class Vote(BaseModel): 
    post_id : int 
    direction : int = conint(ge= 0, le=1)

    

