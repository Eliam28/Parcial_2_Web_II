from sqlmodel import select
from dependencies.dependencies import SessionDep
from pwdlib import PasswordHash
from database.User import User
import jwt
from config import SECRET_KEY, ALGORITHM
from datetime import datetime,timedelta,timezone

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummypassword")

def get_password_hash(password):
    return password_hash.hash(password)

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def authenticate_user(username:str, password:str, session: SessionDep):
    user = session.exec(select(User).where(User.userName == username)).first()
    if not user:
      verify_password(password, DUMMY_HASH)
      return False
    password_correct = verify_password(password,user.password)
    if not password_correct:
      return False
    return user
  
def create_acces_token(data:dict, expires_delta:timedelta|None = None):
  to_encode = data.copy()
  expires_delta = expires_delta if expires_delta else timedelta(minutes=15)
  expire = datetime.now(timezone.utc) + expires_delta
  to_encode.update({"exp":expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt