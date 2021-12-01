from datetime import datetime, timedelta
from typing import Dict

from fastapi import status, Request
from fastapi.exceptions import HTTPException


class ThrottlingException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too Many Rquest",
            headers={"WWW-Authenticate": "Bearer"}
        )


class RateLimit:
    def __init__(self, count: int,
                 period: float = 1000) -> None:
        self.count = count
        self.period = period

    @property
    def inverse(self) -> float:
        return self.period / self.count


class gcra:
    """
    Generic Cell Rate Algorithm
    Reference: https://smarketshq.com/implementing-gcra-in-python-5df1f11aaa96
    """

    def get_tat(self, key: str) -> float:
        # This should return a previous tat for the key or the current time.
        pass

    def set_tat(self, key: str, tat: float) -> None:
        pass

    def update(self, key: str, limit: RateLimit) -> bool:
        now = datetime.now().timestamp()
        tat = max(self.get_tat(key), now)
        separation = (tat - now)
        max_interval = limit.period - limit.inverse
        if separation > max_interval:
            reject = True
        else:
            reject = False
            new_tat = max(tat, now) + limit.inverse
            self.set_tat(key, new_tat)
        return reject


class gcraMemory(gcra):

    def __init__(self):
        self.sessions: Dict[str, float] = {}

    def get_tat(self, key: str) -> float:
        if key not in self.sessions:
            return datetime.now().timestamp() - 100
        return self.sessions[key]

    def set_tat(self, key: str, tat: float) -> None:
        self.sessions[key] = tat


class Throttling():

    def __init__(self,
                 rt: RateLimit = RateLimit(2, timedelta(0, 60, 0, 0)),
                 gcra: gcra = gcraMemory(), ) -> None:
        self.ratelimit = rt
        self.gcra = gcra

    async def __call__(self, request: Request) -> None:
        """
        User ip address as a default key value.
        But if user is authenticated, token will be used as a key
        """
        key = request.client.host
        authorization: str = request.headers.get("Authorization")
        if authorization:
            _, _, key = authorization.partition(" ")
        if self.gcra.update(key, self.ratelimit):
            raise ThrottlingException()
