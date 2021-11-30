from fastapi import APIRouter, Depends, status, HTTPException
import requests

from app.config import API_KEY, API_URL
from app.helper.auth import get_current_user
from app.helper.throttling import Throttling, RateLimit
from app.helper.database import stock_db, StockNotFoundException

throttling = Throttling(rt=RateLimit(4))

router = APIRouter(dependencies=[Depends(get_current_user),
                   Depends(throttling)])

URL = f"{API_URL}?" \
      f"function=TIME_SERIES_DAILY&outputsize=compact&apikey={API_KEY}"


@router.get("/stocks")
async def get_stocks():
    return stock_db.get_all()


@router.get("/stocks/{stock_id}")
async def get_stock_id(stock_id: str):
    try:
        _ = stock_db.get(stock_id)
    except StockNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    url = URL + f"symbol={stock_id}"
    response = requests.get(url)
    return response.json()
