from flask_login import UserMixin
from app import login
from .queries import queries

class User(UserMixin):
    def __init__(self, id, username, password, accid):
        self.id = id
        self.username = username
        self.password = password
        self.accid = accid

    def __repr__(self):
        return f'<User: {self.username}>'
    
    def get_id(self):
        return self.id
    
    def get_username(self):
        return self.username