from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from pydantic import BaseModel

class UserRegister(SQLModel):
    userName: str = Field(min_length=3, max_length=30)
    full_name: str = Field(min_length=3, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6)

class UserResponse(SQLModel):
    id: int
    userName: str
    full_name: str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str