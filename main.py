from dotenv import load_dotenv
from fastapi import FastAPI
from auth_router import auth_router
from order_router import order_router
from fastapi.security import OAuth2PasswordBearer
import os 
from passlib.context import CryptContext

load_dotenv()




app = FastAPI()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")


app.include_router(auth_router)
app.include_router(order_router)


