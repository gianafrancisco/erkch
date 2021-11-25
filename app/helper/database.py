from typing import Dict

from app.models.user import UserInDB

class UserNotFoundException(Exception):
    pass

class UserExistsException(Exception):
    pass

class Database():
    def __init__(self):
        self.users: Dict[str, UserInDB] = {}
    
    def get(self, username):
        if not username in self.users:
            raise UserNotFoundException
        return self.users[username]

    def add(self, user: UserInDB):
        if user.username in self.users:
            raise UserExistsException
        self.users[user.username] = user
        return user


db = Database()
