from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from dotenv import load_dotenv
from .routers import post, user
import os

# uvicorn app.main:app --reload  

load_dotenv()
db_host = os.getenv("DB_HOST")
db_db = os.getenv("DB_DB")
db_user = os.getenv("DB_USER")
db_pass = os.getenv("DB_PASS")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:

    try:
        conn = psycopg2.connect(host=db_host, database=db_db, user=db_user, 
            password=db_pass, cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database successfully connected")
        break
    except Exception as error:
        print("Database connection failed")
        print("Error: ", error)
        time.sleep(2)

app.include_router(post.router)

@app.get("/")
def root():
    return {"message": "Server root"}


