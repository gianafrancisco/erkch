from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer

from .routers import users, stocks, health

app = FastAPI()

app.include_router(users.router)
app.include_router(stocks.router)
app.include_router(health.router)
