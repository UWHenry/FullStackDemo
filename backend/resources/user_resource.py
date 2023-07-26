from db_utils.user_manager import UserManager, argon2
from flask import request
from flask_restx import Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from .namespace_models import (
    api_ns,
    message_output_model,
    access_token_model,
    user_signup_input_model,
    user_login_input_model,
    user_update_input_model,
    user_search_input_model,
    user_search_output_model,
    user_model
)


# sign up and login
@api_ns.route('/signup')
class SignUp(Resource):
    @api_ns.expect(user_signup_input_model)
    @api_ns.response(model=access_token_model, code=200, description="Access token")
    @api_ns.response(model=message_output_model, code=400, description="Invalid json body")
    @api_ns.response(model=message_output_model, code=409, description="User already Exists")
    def post(self):
        data = request.get_json()
        username = data.get("username", None)
        password = data.get("password", None)
        address = data.get("address", "")
        roles = data.get("roles", [])
        if not username or not password:
            return {"message": "Invalid json body"}, 400
        new_user = UserManager.create(username, password, address, roles)
        if new_user:
            access_token = create_access_token(identity=username)
            return {'access_token': access_token}, 200
        return {"message": "User already exists"}, 409

@api_ns.route('/login')
class Login(Resource):
    @api_ns.expect(user_login_input_model)
    @api_ns.response(model=access_token_model, code=200, description="Access token")
    @api_ns.response(model=message_output_model, code=401, description="Invalid credentials")
    def post(self):
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        user = UserManager.read(username)
        if user and argon2.check_password_hash(user.password, password):
            access_token = create_access_token(identity=username)
            return {"access_token": access_token}, 200
        return {"message": "Invalid credentials"}, 401

# User Read, Update, Delete
@api_ns.route('/user/<string:username>')
class UserResource(Resource):
    @api_ns.param('username', 'The username of the user to read', type='string', required=True)
    @api_ns.response(model=user_model, code=200, description="User model")
    @api_ns.response(model=message_output_model, code=404, description="User not found")
    @jwt_required()
    def get(self, username: str):
        result_user = UserManager.read(username)
        if result_user:
            return result_user.as_dict(), 200
        return {"message": "User not found"}, 404

    @api_ns.param('username', 'The username of the user to update', type='string', required=True)
    @api_ns.expect(user_update_input_model)
    @api_ns.marshal_with(message_output_model, code=200, description="Success")
    @api_ns.marshal_with(message_output_model, code=400, description="Password cannot be empty string")
    @api_ns.marshal_with(message_output_model, code=404, description="User not found")
    @api_ns.marshal_with(message_output_model, code=500, description="Fail")
    @jwt_required()
    def put(self, username: str):
        data = request.get_json()
        password = data.get("password", None)
        address = data.get("address", None)
        roles = data.get("roles", None)
        if password == "":
            return {"message": "Password cannot be empty string"}, 400

        user = UserManager.read(username)
        if user is None:
            return {"message": "User not found"}, 404
        updated_user = UserManager.update(
            username, user.version_id, password, address, roles)
        if updated_user:
            return {"message": "Success"}, 200
        return {"message": "Fail"}, 500

    @api_ns.param('username', 'The username of the user to delete', type='string', required=True)
    @api_ns.marshal_with(message_output_model, code=200, description="Success")
    @api_ns.marshal_with(message_output_model, code=404, description="User not found")
    @api_ns.marshal_with(message_output_model, code=500, description="Fail")
    @jwt_required()
    def delete(self, username: str):
        user = UserManager.read(username)
        if user is None:
            return {"message": "User not found"}, 404
        success = UserManager.delete(username)
        if success:
            return {"message": "Success"}, 200
        return {"message": "Fail"}, 500

# Search Users
@api_ns.route('/users/search')
class UserSearchResource(Resource):
    @api_ns.expect(user_search_input_model)
    @api_ns.marshal_list_with(user_search_output_model, code=200)
    @jwt_required()
    def post(self):
        data = request.get_json()
        page = data.get('page', 1)
        page_size = data.get('page_size', 10)
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10

        sort_by = data.get('sort_by', 'username')
        reverse = data.get('reverse', False)
        search_username = data.get('search_username', None)
        search_address = data.get('search_address', None)
        user_list = UserManager.search(
            page, page_size, sort_by, reverse, search_username, search_address)
        user_list = [user.as_dict() for user in user_list]
        
        total_items = UserManager.count()
        total_pages = (total_items + page_size - 1) // page_size
        return {"users": user_list, "total_pages": total_pages}, 200

# List Users
@api_ns.route('/users')
class UserListResource(Resource):
    @api_ns.marshal_list_with(user_model, code=200)
    @jwt_required()
    def get(self):
        user_list = UserManager.list()
        user_list = [user.as_dict() for user in user_list]
        return user_list, 200