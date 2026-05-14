from sqlmodel import SQLModel,Field

class User(SQLModel, table = True):
    id: int | None = Field(default=None, primary_key=True)
    userName: str = Field(unique=True, index=True)
    full_name: str
    email: str = Field(unique=True, index=True)
    password: str