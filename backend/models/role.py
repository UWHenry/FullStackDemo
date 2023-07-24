from . import db

class Role(db.Model):
    __tablename__ = "roles"
    
    rolename = db.Column(db.String, primary_key=True, index=True)
    permission = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    version_id = db.Column(db.Integer, nullable=False, default=0)
        
    def get_id(self):
        return str(self.rolename)