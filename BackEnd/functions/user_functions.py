from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from config import SECRET_KEY, ALGORITHM
from pydantic import BaseModel
from dependencies.dependencies import SessionDep
from database.User import User
from schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_user(username: str, session: SessionDep):
  user = session.select(User).where(User.userName == username).first()
  return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")

    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except InvalidTokenError:
    raise credentials_exception
  user = get_user(username=token_data.username, session=session)
  if user is None:
    raise credentials_exception
  return user