from sqlmodel import SQLModel, Field
from pydantic import EmailStr

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