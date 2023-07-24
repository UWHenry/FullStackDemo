from db_utils import user_manager, argon2
from flask import request
from flask_restx  import Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from . import ns

# models for swagger
role_model = ns.model("User's Roles Field", {
    'rolename': fields.String(required=True, description='The role name'),
    'permission': fields.String(required=True, description='The role permission'),
    'description': fields.String(required=True, description='The role description')
})
user_model = ns.model('User Model', {
    'username': fields.String(required=True, description='The user username'),
    'address': fields.String(required=True, description='The user address'),
    'roles': fields.List(fields.Nested(role_model), required=True, description='List of user roles')
})
user_update_input = ns.model('User Update Input', {
    'password': fields.String(required=False, description='The user password'),
    'address': fields.String(required=False, description='The user address'),
    'roles': fields.List(fields.String(required=False, description="role name"), required=False, description="The user roles")
})
user_signup_input = ns.model('User Signup Input', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
    'address': fields.String(required=True),
    'roles': fields.List(fields.String(required=False, description="role name"), required=False, description="The user roles")
})
user_login_input = ns.model('User Login Input', {
    'username': fields.String(required=True),
    'password': fields.String(required=True),
})
user_list_input = ns.model('User List Input', {
    "page": fields.Integer(required=False),
    "page_size": fields.Integer(required=False),
    "sort_by": fields.String(required=False),
    "reverse": fields.String(required=False),
    "search_username": fields.String(required=False),
    "search_address": fields.String(required=False)
})

users = user_manager.UserManager

# sign up and login
@ns.route('/signup')
class SignUp(Resource):
    @ns.expect(user_signup_input)
    @ns.marshal_with(None, code=200, description="Access token")
    @ns.marshal_with(None, code=400, description="Invalid json body")
    @ns.marshal_with(None, code=409, description="User already Exists")
    def post(self, username: str, password: str, address: str):
        data = request.get_json()
        username = data.get("username", None)
        password = data.get("password", None)
        address = data.get("address", "")
        roles = data.get("roles", [])
        if not username or not password:
            return {"message": "Invalid json body"}, 400
        new_user = users.create(username, password, address, roles)
        if new_user:
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        return {"message": "User already exists"}, 409

@ns.route('/login')
class Login(Resource):
    @ns.expect(user_login_input)
    @ns.marshal_with(None, code=200, description="Access token")
    @ns.marshal_with(None, code=401, description="Invalid credentials")
    def post(self, username: str, password: str):
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        password_hash = argon2.generate_password_hash(password)
        user = users.read(username)
        if user and user.username == username and user.password == password_hash:
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401
    
# User Read, Update, Delete
@ns.route('/user')
class UserResource(Resource):
    @ns.marshal_with(user_model, code=200)
    @ns.marshal_with(None, code=404, description="User not found")
    @jwt_required()
    def get(self):
        username = get_jwt_identity()
        result_user = users.read(username)
        if result_user:
            return result_user.as_dict(), 200
        return {"message": "User not found"}, 404
    
    @ns.expect(user_update_input)
    @ns.marshal_with(None, code=200, description="Success")
    @ns.marshal_with(None, code=400, description="Password cannot be empty string")
    @ns.marshal_with(None, code=404, description="User not found")
    @ns.marshal_with(None, code=500, description="Fail")
    @jwt_required()
    def put(self):
        data = request.get_json()
        username = get_jwt_identity()
        password = data.get("password", None)
        address = data.get("address", None)
        roles = data.get("roles", None)
        if password == "":
            return {"message": "Password cannot be empty string"}, 400
        message = users.update(username, password, address, roles)
        if message == "Success":
            return {"message": "Success"}, 200
        if message == "User not found":
            return {"message": "User not found"}, 404
        return {"message": "Fail"}, 500
    
    @ns.marshal_with(None, code=200, description="Success")
    @ns.marshal_with(None, code=404, description="User not found")
    @ns.marshal_with(None, code=500, description="Fail")
    @jwt_required()
    def delete(self, username: str):
        username = get_jwt_identity()
        message = users.delete(username)
        if message == "Success":
            return {"message": "Success"}, 200
        if message == "User not found":
            return {"message": "User not found"}, 404
        return {"message": "Fail"}, 500

# List Users
@ns.route('/users')
class UserListResource(Resource):
    @ns.expect(user_list_input)
    @ns.marshal_list_with(user_model, code=200)
    @jwt_required()
    def post(self):
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
        page_size = int(request.args.get('page_size', 10))
        if page_size < 1:
            page_size = 10
        sort_by = request.args.get('sort_by', 'username')
        reverse = request.args.get('reverse', "") == "true"
        search_username = request.args.get('search_username', None)
        search_address = request.args.get('search_address', None)
        user_list = users.list(page, page_size, sort_by, reverse, search_username, search_address)
        user_list = [user.as_dict() for user in user_list]
        return user_list, 200