from typing import Annotated
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlmodel import select
from config import SECRET_KEY, ALGORITHM
from dependencies.dependencies import SessionDep
from database.User import User
from schemas.auth import TokenData

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)

def get_user(username: str, session: SessionDep):
  query = select(User).where(User.userName == username)
  user = session.exec(query).first()
  return user

async def get_current_user(request: Request, token: Annotated[str | None, Depends(oauth2_scheme)] = None, session: SessionDep = None):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  time_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired", headers={"WWW-Authenticate": "Bearer"})

  if token is None:
    token = request.cookies.get("access_token")
  
  if token is None:
    raise credentials_exception

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")

    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except ExpiredSignatureError:
    raise time_exception
  except InvalidTokenError:
    raise credentials_exception
  user = get_user(username=token_data.username, session=session)
  if user is None:
    raise credentials_exception
  return user