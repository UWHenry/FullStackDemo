from models import db
from models.role import Role
from typing import List


class RoleManager:
    @staticmethod
    def create(rolename: str, permission: str, description: str) -> Role | None:
        try:
            db.session.begin()
            new_role = Role(
                rolename=rolename,
                permission=permission,
                description=description
            )
            db.session.add(new_role)
            db.session.commit()
            return new_role
        except:
            db.session.rollback()
        return None

    @staticmethod
    def read(rolename: str) -> Role | None:
        role = Role.query.get(rolename)
        return role

    @staticmethod
    def update(rolename: str, version_id: int, permission: str | None, description: str | None) -> Role | None:
        try:
            db.session.begin()
            role = Role.query.get(rolename)
            if role:
                if version_id < role.version_id:
                    raise Exception(
                        "Optimistic Lock Triggered: Abort Transaction!")
                if permission is not None:
                    role.permission = permission
                if description is not None:
                    role.description = description
                role.version_id += 1
                db.session.commit()
                return role
        except:
            db.session.rollback()
        return None

    @staticmethod
    def delete(rolename: str) -> bool:
        try:
            db.session.begin()
            role = Role.query.get(rolename)
            if role:
                db.session.delete(role)
                db.session.commit()
                return True
        except:
            db.session.rollback()
        return False

    @staticmethod
    def search(page: int = 1, page_size: int = 10, order_by: str = "rolename", reverse: bool = False, search_rolename: str | None = None, search_permission: str | None = None, search_description: str | None = None) -> List[Role]:
        query = Role.query
        if search_rolename:
            query = query.filter(Role.rolename.ilike(f'%{search_rolename}%'))
        if search_permission:
            query = query.filter(
                Role.permission.ilike(f'%{search_permission}%'))
        if search_description:
            query = query.filter(
                Role.description.ilike(f'%{search_description}%'))

        order = Role.rolename
        if order_by == "permission":
            order = Role.permission
        elif order_by == "description":
            order = Role.description
        if reverse:
            order = order.desc()
        query = query.order_by(order)

        start_idx = (page - 1) * page_size
        roles_page = query.offset(start_idx).limit(page_size).all()
        return roles_page

    @staticmethod
    def list() -> List[Role]:
        return Role.query.all()
    
    @staticmethod
    def count() -> int:
        return Role.query.count()
