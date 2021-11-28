from fastapi import FastAPI

from app.routers import users, stocks, health

app = FastAPI()

app.include_router(users.router)
app.include_router(stocks.router)
app.include_router(health.router)
