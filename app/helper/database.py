from typing import Dict

from app.models.user import UserInDB


class UserNotFoundException(Exception):
    pass


class UserExistsException(Exception):
    pass


class Database():
    def get(self, username) -> UserInDB:
        pass

    def add(self, user: UserInDB) -> None:
        pass


class MemoryDB(Database):
    def __init__(self):
        self.users: Dict[str, UserInDB] = {}

    def get(self, username) -> UserInDB:
        if username not in self.users:
            raise UserNotFoundException
        return self.users[username]

    def add(self, user: UserInDB) -> None:
        if user.username in self.users:
            raise UserExistsException
        self.users[user.username] = user
        return user


db = MemoryDB()
