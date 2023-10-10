from math import ceil
from typing import Tuple
from models import db
from models.role import Role
from models.user import User


class RoleManager:
    @staticmethod
    def _get_user_list(users: list[str]) -> list[User]:
        return User.query.filter(User.username.in_(users)).all()
    
    @staticmethod
    def create(rolename: str, permission: str, description: str, users: list[str]):
        new_role = Role(
            rolename=rolename,
            permission=permission,
            description=description,
            users=RoleManager._get_user_list(users)
        )
        db.session.add(new_role)

    @staticmethod
    def read(rolename: str) -> Role | None:
        return db.session.get(Role, rolename)

    @staticmethod
    def update(role: Role, permission: str | None, description: str | None, users: list[str] | None):
        if permission is not None:
            role.permission = permission
        if description is not None:
            role.description = description
        if users is not None:
            role.users = RoleManager._get_user_list(users)
        role.version_id += 1

    @staticmethod
    def delete(role: Role):
        db.session.delete(role)

    @staticmethod
    def search(
        page: int = 1, 
        page_size: int = 10, 
        order_by: str = "rolename", 
        reverse: bool = False, 
        search_rolename: str | None = None, 
        search_permission: str | None = None, 
        search_description: str | None = None
    ) -> Tuple[list[Role], int]:
        query = Role.query
        if search_rolename:
            query = query.filter(Role.rolename.ilike(f'%{search_rolename}%'))
        if search_permission:
            query = query.filter(Role.permission.ilike(f'%{search_permission}%'))
        if search_description:
            query = query.filter(Role.description.ilike(f'%{search_description}%'))

        order = Role.rolename
        if order_by == "permission":
            order = Role.permission
        elif order_by == "description":
            order = Role.description
        if reverse:
            order = order.desc()
        query = query.order_by(order)
        
        total_roles = query.count()
        total_pages = ceil(total_roles / page_size)

        start_idx = (page - 1) * page_size
        roles_page = query.offset(start_idx).limit(page_size).all()
        return roles_page, total_pages

    @staticmethod
    def list() -> list[Role]:
        return Role.query.all()
