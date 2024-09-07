from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class PostBase(BaseModel):
    title: str
    content: str
    published: bool= True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Posts: Post
    votes: int
    
    class Config:
        orm_mode = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Vote(BaseModel):
    post_id: int
    dir: int = Field(le=1)