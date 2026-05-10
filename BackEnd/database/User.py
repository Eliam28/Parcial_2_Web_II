from sqlmodel import SQLModel,Field
from typing import TYPE_CHECKING, Optional

class User(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    userName: str = Field(min_length=3,max_length=100, unique=True)
    full_name: str = Field(min_length=3, max_length=100)
    email: str = Field(unique=True)
    password: str