from fastapi import APIRouter, Depends

from app.config import API_KEY, API_URL
from app.helper.auth import get_current_user
from app.helper.throttling import Throttling, RateLimit
from app.helper.database import stock_db

throttling = Throttling(rt=RateLimit(4))

router = APIRouter(dependencies=[Depends(get_current_user),
                   Depends(throttling)])

url = '{}?' \
      'function=TIME_SERIES_DAILY&symbol=FB&outputsize=compact&apikey={}' \
      .format(API_URL, API_KEY)


@router.get("/stocks")
async def get_stocks():
    return stock_db.get_all()
