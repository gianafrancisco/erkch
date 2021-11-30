from typing import Dict

from pydantic import BaseModel

from app.models.user import UserInDB
from app.models.stock import Stock


class UserNotFoundException(Exception):
    pass


class UserExistsException(Exception):
    pass


class Database():
    def get(self, id) -> BaseModel:
        pass

    def add(self, model: BaseModel) -> None:
        pass

    def get_all(self) -> Dict[str, BaseModel]:
        pass


class UserMemoryDB(Database):
    def __init__(self):
        self.__users: Dict[str, UserInDB] = {}

    def get(self, id) -> UserInDB:
        if id not in self.__users:
            raise UserNotFoundException
        return self.__users[id]

    def add(self, user: UserInDB) -> None:
        if user.username in self.__users:
            raise UserExistsException
        self.__users[user.username] = user
        return user


class StockMemoryDB(Database):
    def __init__(self):
        self.__stock: Dict[str, Stock] = {}

    def get(self, id) -> Stock:
        if id not in self.__stock:
            raise UserNotFoundException
        return self.__stock[id]

    def add(self, model: Stock) -> None:
        if model.id in self.__stock:
            raise UserExistsException
        self.__stock[model.id] = model
        return model

    def get_all(self) -> Dict[str, Stock]:
        return self.__stock.copy()


db = UserMemoryDB()
stock_db = StockMemoryDB()
stock_db.add(Stock(id="FB", name="Facebook"))
stock_db.add(Stock(id="AAPL", name="Apple"))
stock_db.add(Stock(id="MSFT", name="Microsoft"))
stock_db.add(Stock(id="GOOGL", name="Google"))
stock_db.add(Stock(id="AMZN", name="Amazon"))
