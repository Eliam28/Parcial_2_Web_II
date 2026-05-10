from fastapi import FastAPI
from sqlmodel import SQLModel
from database.db import engine
from contextlib import asynccontextmanager

def create_db_and_tables():
 SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
 create_db_and_tables()
 yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def saludo():
 return {"saludo":"hola"}