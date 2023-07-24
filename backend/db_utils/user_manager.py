from models import db
from models.user import User
from . import argon2
from typing import Union, Literal

class UserManager:
    @staticmethod
    def create(username: str, password: str, address: str) -> User | None:
        try:
            db.session.begin()
            password_hash = argon2.generate_password_hash(password)
            new_user = User(
                username = username,
                password = password_hash,
                address = address
            )
            db.session.add(new_user)
            db.session.commit()
            return new_user
        except:
            db.session.rollback()
        return None

    @staticmethod
    def read(username: str) -> User | None:
        user = User.query.get(username)
        return user

    @staticmethod
    def update(username: str, password: str | None, address: str | None) -> Union[Literal["Success"], Literal["User not found"], Literal["Fail"]]:
        try:
            db.session.begin()
            user = User.query.get(username)
            if user:
                if password:
                    password_hash = argon2.generate_password_hash(password)
                    user.password = password_hash
                if address:
                    user.address = address
                db.session.commit()
                return "Success"
            return "User not found"
        except:
            db.session.rollback()
        return "Fail"

    @staticmethod
    def delete(username: str) -> Union[Literal["Success"], Literal["User not found"], Literal["Fail"]]:
        try:
            db.session.begin()
            user = User.query.get(username)
            if user:
                db.session.delete(user)
                db.session.commit()
                return "Success"
            return "User not found"
        except:
            db.session.rollback()
        return "Fail"

    @staticmethod
    def list(page: int = 1, page_size: int = 10, order_by: str = "username", reverse: bool = False, search_username: str | None = None, search_address: str | None = None) -> list[User]:
        query = User.query
        if search_username:
            query = query.filter(User.username.like(f'%{search_username}%'))
        if search_address:
            query = query.filter(User.address.like(f'%{search_address}%'))
        
        order = User.username
        if order_by == "address":
            order = User.address
        if reverse:
            order = order.desc()
        query = query.order_by(order)
            
        start_idx = (page - 1) * page_size
        users_page = query.offset(start_idx).limit(page_size).all()
        return users_page