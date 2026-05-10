from sqlmodel import Session
from typing import Annotated
from database.db import engine
from fastapi import Depends

def get_sessions():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session,Depends(get_sessions)]