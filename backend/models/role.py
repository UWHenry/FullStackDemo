from . import db


class Role(db.Model):
    __tablename__ = "roles"
    rolename = db.Column(db.String, primary_key=True, index=True)
    permission = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    users = db.relationship('User', secondary='user_roles', back_populates='roles')
    version_id = db.Column(db.Integer, nullable=False, default=0)

    def get_id(self):
        return str(self.rolename)

    def as_dict(self):
        return {
            "rolename": self.rolename,
            "permission": self.permission,
            "description": self.description,
            "users": [
                {
                    "username": user.name,
                    "address": user.address
                }
                for user in self.users
            ]
        }
