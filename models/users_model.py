from sqlalchemy import Column, Integer, String
from database import db


class User(db.Models):
    __tablename__ = 'users'
    id_user = db.Column(Integer, primary_key=True)
    username = db.Column(String(50), unique=True, nullable=False)
    password = db.Column(String(200), nullable=False)

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password
