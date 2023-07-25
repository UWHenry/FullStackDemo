from . import db

# Association Table for User and Role many-to-many relationship
user_roles = db.Table('user_roles',
    db.Column('user_username', db.String, db.ForeignKey('users.username'), primary_key=True),
    db.Column('role_rolename', db.String, db.ForeignKey('roles.rolename'), primary_key=True)
)