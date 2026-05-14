from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError
from sqlmodel import select
from config import SECRET_KEY, ALGORITHM
from dependencies.dependencies import SessionDep
from database.User import User
from schemas.auth import TokenData
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user(username: str, session: SessionDep):
  query = select(User).where(User.userName == username)
  user = session.exec(query).first()
  return user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: SessionDep):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  time_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    expire = payload.get("exp")
    
    if expire is None or datetime.fromtimestamp(expire) < datetime.now():
      raise time_exception

    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except InvalidTokenError:
    raise credentials_exception
  user = get_user(username=token_data.username, session=session)
  if user is None:
    raise credentials_exception
  return user