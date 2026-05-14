from fastapi import APIRouter, Depends
from typing import Annotated
from database.User import User
from functions.user_functions import get_current_user

router = APIRouter(tags=["User"], prefix="/users")

@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
  
  return current_user