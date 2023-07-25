from . import db

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True, index=True)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary='user_roles', back_populates='users')
    version_id = db.Column(db.Integer, nullable=False, default=0)

    def get_id(self):
        return str(self.username)

    def as_dict(self):
        return {
            "username": str(self.username),
            "address": self.address,
            "roles": [
                {
                    "rolename": role.rolename,
                    "permission": role.permission,
                    "description": role.description
                }
                for role in self.roles
            ]
        }
