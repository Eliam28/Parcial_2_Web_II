from fastapi import APIRouter, HTTPException, status
from sqlmodel import select
from database.User import User
from dependencies.dependencies import SessionDep
from typing import Any

router = APIRouter(prefix="/test/user", tags=["Test User"])

@router.get("/", status_code=status.HTTP_200_OK)
def get_all(session: SessionDep):
    users = session.exec(select(User)).all()
    result = []

    for user in users:
        result.append({
            "id": user.id,
            "userName": user.userName,
            "name": user.full_name,
            "email": user.email,
            "password": user.password
        })
    return result

@router.post("/", status_code= status.HTTP_201_CREATED)
def create_user_test(session: SessionDep, user:User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user