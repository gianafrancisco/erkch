from typing import Counter
from fastapi.exceptions import HTTPException
from starlette.requests import Request
from starlette.status import HTTP_429_TOO_MANY_REQUESTS

class Throttling():

    counter = 10

    async def __call__(self, request: Request):
        if Throttling.counter == 0:
            raise HTTPException(
                status_code=HTTP_429_TOO_MANY_REQUESTS,
                detail="Not authenticated",
                headers={"WWW-Authenticate": "Bearer"},
            )
        Throttling.counter -= 1

throttling = Throttling()