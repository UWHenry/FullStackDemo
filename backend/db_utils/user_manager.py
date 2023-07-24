from models import db
from models.user import User
from . import argon2


class UserManager:
    @staticmethod
    def create(username: str, password: str, address: str) -> bool:
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
            return True
        except:
            db.session.rollback()
        return False

    @staticmethod
    def read(username: str) -> User | None:
        user = User.query.get(username)
        return user

    @staticmethod
    def update(username: str, password: str | None, address: str | None) -> bool:
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
                return True
        except:
            db.session.rollback()
        return False

    @staticmethod
    def delete(username: str) -> bool:
        try:
            db.session.begin()
            user = User.query.get(username)
            if user:
                db.session.delete(user)
                db.session.commit()
                return True
        except:
            db.session.rollback()
        return False

    @staticmethod
    def list() -> list[User]:
        users = User.query.all()
        return users