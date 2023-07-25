from models import db
from models.user import User
from models.role import Role
from . import argon2
from typing import List


class UserManager:
    @staticmethod
    def _get_role_list(roles: List[str]):
        role_list = []
        for rolename in roles:
            role = Role.query.get(rolename)
            if role and role not in role_list:
                role_list.append(role)
        return role_list

    @staticmethod
    def create(username: str, password: str, address: str, roles: List[str]) -> User | None:
        try:
            db.session.begin()
            password_hash = argon2.generate_password_hash(password)
            new_user = User(
                username=username,
                password=password_hash,
                address=address,
                roles=UserManager._get_role_list(roles)
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
    def update(username: str, version_id: int, password: str | None, address: str | None, roles: List[str] | None) -> User | None:
        try:
            db.session.begin()
            user = User.query.get(username)
            if user:
                if version_id < user.version_id:
                    raise Exception("Optimistic Lock Triggered: About Transaction!")
                if password:
                    password_hash = argon2.generate_password_hash(password)
                    user.password = password_hash
                if address is not None:
                    user.address = address
                if roles is not None:
                    user.roles = UserManager._get_role_list(roles)
                user.version_id += 1
                db.session.commit()
                return user
        except:
            db.session.rollback()
        return None

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
    def search(page: int = 1, page_size: int = 10, order_by: str = "username", reverse: bool = False, search_username: str | None = None, search_address: str | None = None) -> List[User]:
        query = User.query
        if search_username:
            query = query.filter(User.username.ilike(f'%{search_username}%'))
        if search_address:
            query = query.filter(User.address.ilike(f'%{search_address}%'))

        order = User.username
        if order_by == "address":
            order = User.address
        if reverse:
            order = order.desc()
        query = query.order_by(order)

        start_idx = (page - 1) * page_size
        users_page = query.offset(start_idx).limit(page_size).all()
        return users_page

    @staticmethod
    def list() -> List[User]:
        return User.query.all()