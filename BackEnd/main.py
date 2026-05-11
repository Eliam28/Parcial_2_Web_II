from fastapi import FastAPI, HTTPException, status, Depends
from sqlmodel import SQLModel
from database.db import engine
from contextlib import asynccontextmanager

from sqlmodel import select
from pwdlib import PasswordHash
from database.User import User
from schemas.auth import UserRegister, UserResponse, Token
from dependencies.dependencies import SessionDep

from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta,timezone
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware

def create_db_and_tables():
 SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
 create_db_and_tables()
 yield

load_dotenv()
SECRET_KEY= os.getenv("SECRET_KEY")
ALGORITHM= os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

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
  
@app.get("/")
def saludo():
 return {"saludo":"hola"}

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
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

@app.post("/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: SessionDep) -> Token:
  user = authenticate_user(form_data.username, form_data.password, session)
  if not user:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate":"Bearer"})
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_acces_token(data={"sub": user.userName}, expires_delta=access_token_expires)
  return Token(access_token=access_token, token_type="bearer")
