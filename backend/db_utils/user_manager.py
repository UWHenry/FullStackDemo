from math import ceil
from typing import Tuple
from models import db
from models.user import User
from models.role import Role
from flask_argon2 import Argon2


argon2 = Argon2()

class UserManager:
    @staticmethod
    def _get_role_list(roles: list[str]) -> list[Role]:
        return Role.query.filter(Role.rolename.in_(roles)).all()

    @staticmethod
    def create(username: str, password: str, address: str, roles: list[str]):
        password_hash = argon2.generate_password_hash(password)
        new_user = User(
            username=username,
            password=password_hash,
            address=address,
            roles=UserManager._get_role_list(roles)
        )
        db.session.add(new_user)

    @staticmethod
    def read(username: str) -> User | None:
        return User.query.get(username)

    @staticmethod
    def update(user: User, password: str | None, address: str | None, roles: list[str] | None):
        if password:
            password_hash = argon2.generate_password_hash(password)
            user.password = password_hash
        if address is not None:
            user.address = address
        if roles is not None:
            user.roles = UserManager._get_role_list(roles)
        user.version_id += 1

    @staticmethod
    def delete(user: User):
        db.session.delete(user)
        
    @staticmethod
    def search(
        page: int = 1, 
        page_size: int = 10, 
        order_by: str = "username", 
        reverse: bool = False, 
        search_username: str | None = None, 
        search_address: str | None = None
    ) -> Tuple[list[User], int]:
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
        
        total_users = query.count()
        total_pages = ceil(total_users / page_size)

        start_idx = (page - 1) * page_size
        users_page = query.offset(start_idx).limit(page_size).all()
        return users_page, total_pages

    @staticmethod
    def list() -> list[User]:
        return User.query.all()