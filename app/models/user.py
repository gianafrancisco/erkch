from typing import Optional

from pydantic import BaseModel
from fastapi import Form


class User(BaseModel):
    username: str
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    disabled: Optional[bool] = None


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
