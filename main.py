import os
from dotenv import load_dotenv
from fastapi import FastAPI
from auth_router import auth_router
from order_router import order_router

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

app.include_router(auth_router)
app.include_router(order_router)


