from datetime import timedelta
import requests
from fastapi import APIRouter, Depends

from app.config import API_KEY, API_URL
from app.helper.auth import oauth2_scheme
from app.helper.throttling import Throttling, RateLimit

throttling = Throttling(rt=RateLimit(4))

router = APIRouter(dependencies=[Depends(oauth2_scheme), Depends(throttling)])

url = '{}?' \
      'function=TIME_SERIES_DAILY&symbol=FB&outputsize=compact&apikey={}' \
      .format(API_URL, API_KEY)


@router.get("/stocks")
async def get_stocks():
    r = requests.get(url)
    return r.json()

