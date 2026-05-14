from fastapi import APIRouter, HTTPException, status, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from typing import Annotated
from sqlmodel import select
from database.User import User
from schemas.auth import UserRegister, UserResponse, Token
from dependencies.dependencies import SessionDep
from functions.auth_functions import get_password_hash, authenticate_user, create_acces_token
from config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(tags=["Auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, session: SessionDep):
 
 existing_username = session.exec(select(User).where(User.userName == user.userName)).first()

 if existing_username:
  raise HTTPException( status_code= status.HTTP_400_BAD_REQUEST, detail="El nombre de usuario ya existe")
 
 existing_email = session.exec(select(User).where(User.email == user.email)).first()

 if existing_email:
  raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail="El correo electrónico ya existe")
 
 hashed_password = get_password_hash(user.password)
 
 new_user = User( userName= user.userName, full_name= user.full_name, email= user.email, password=hashed_password)

 session.add(new_user)
 session.commit()
 session.refresh(new_user)
 
 return new_user

@router.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep, response: Response) -> Token:
  user = authenticate_user(form_data.username, form_data.password, session)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate":"Bearer"})
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_acces_token(data={"sub": user.userName}, expires_delta=access_token_expires)

  response.set_cookie(key="access_token", value=access_token,httponly=True, max_age=180,secure=False,samesite="lax")

  return Token(access_token=access_token, token_type="bearer")