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
                 period: timedelta = timedelta(seconds=1)) -> None:
        self.count = count
        self.period = period

    @property
    def inverse(self) -> float:
        return self.period.total_seconds() / self.count


class gcra:
    """
    Generic Cell Rate Algorithm
    Reference: https://smarketshq.com/implementing-gcra-in-python-5df1f11aaa96
    """

    def get_tat(self, key: str) -> datetime:
        # This should return a previous tat for the key or the current time.
        pass

    def set_tat(self, key: str, tat: datetime) -> None:
        pass

    def update(self, key: str, limit: RateLimit) -> bool:
        now = datetime.utcnow()
        tat = max(self.get_tat(key), now)
        separation = (tat - now).total_seconds()
        max_interval = limit.period.total_seconds() - limit.inverse
        if separation > max_interval:
            reject = True
        else:
            reject = False
            new_tat = max(tat, now) + timedelta(seconds=limit.inverse)
            self.set_tat(key, new_tat)
        return reject


class gcraMemory(gcra):

    def __init__(self):
        self.sessions: Dict[str, datetime] = {}

    def get_tat(self, key: str) -> datetime:
        if key not in self.sessions:
            return datetime.now()
        return self.sessions[key]

    def set_tat(self, key: str, tat: datetime) -> None:
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
