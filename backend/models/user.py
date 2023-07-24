from . import db


# Association Table
user_roles = db.Table('user_roles',
    db.Column('user_username', db.String, db.ForeignKey('users.username'), primary_key=True),
    db.Column('role_rolename', db.String, db.ForeignKey('roles.rolename'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.String, primary_key=True, index=True)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users', lazy=True))
    version_id = db.Column(db.Integer, nullable=False, default=0)
    
    def get_id(self):
        return str(self.username)