# pyrefly: ignore [missing-import]
from pydantic._internal._known_annotated_metadata import schemas
# pyrefly: ignore [missing-import]
from passlib.context import CryptContext
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

from auth_router import auth_router
from order_router import order_router

app.include_router(auth_router)
app.include_router(order_router)
