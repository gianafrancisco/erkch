import re
from typing import Optional

from pydantic import BaseModel, validator
from fastapi import Form
from fastapi.exceptions import HTTPException

REGEXP_EMAIL = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


class User(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None

    @validator('email')
    def email_validation(cls, value, values, config, field):
        if not re.fullmatch(REGEXP_EMAIL, value):
            raise HTTPException(
                status_code=422,
                detail='Email is not a valid email address')
        return value


class UserInDB(User):
    hashed_password: str


class SignUpForm():
    def __init__(
        self,
        email: str = Form(...),
        first_name: str = Form(...),
        last_name: str = Form(...),
        password: str = Form(...),
    ):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
