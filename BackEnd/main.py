from fastapi import FastAPI
from sqlmodel import SQLModel
from database.db import engine
from contextlib import asynccontextmanager

from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.userRoute import router as user_router

def create_db_and_tables():
 SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
 create_db_and_tables()
 yield

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:5173"
]

app.add_middleware(
 CORSMiddleware,
 allow_origins=origins,
 allow_credentials=True,
 allow_methods=["*"],
 allow_headers=["*"]
 )
  
@app.get("/")
def saludo():
 return {"saludo":"hola"}

app.include_router(auth_router)
app.include_router(user_router)