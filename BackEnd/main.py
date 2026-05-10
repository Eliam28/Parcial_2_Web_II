from fastapi import FastAPI, HTTPException, status
from sqlmodel import SQLModel
from database.db import engine
from contextlib import asynccontextmanager

from sqlmodel import select
from pwdlib import PasswordHash
from database.User import User
from schemas.auth import UserRegister, UserResponse
from dependencies.dependencies import SessionDep

from fastapi.middleware.cors import CORSMiddleware

def create_db_and_tables():
 SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
 create_db_and_tables()
 yield

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(CORSMiddleware,allow_origins=origins,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)

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