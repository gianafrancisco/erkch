from pydantic import BaseModel


class Stock(BaseModel):
    id: str
    name: str
