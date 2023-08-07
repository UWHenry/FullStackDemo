from db_utils.user_manager import UserManager, argon2
from flask import request, after_this_request
from flask_restx import Resource
from flask_jwt_extended import create_access_token, unset_jwt_cookies, set_access_cookies
from .namespace_models import (
    api_ns,
    message_output_model,
    access_token_model,
    user_signup_input_model,
    user_login_input_model
)

@api_ns.route('/signup')
class SignUp(Resource):
    @api_ns.expect(user_signup_input_model)
    @api_ns.marshal_with(access_token_model, code=200, description="Signup successful")
    @api_ns.marshal_with(message_output_model, code=400, description="Invalid json body")
    @api_ns.marshal_with(message_output_model, code=409, description="User already Exists")
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
            @after_this_request
            def set_access_cookie(response):
                access_token = create_access_token(identity=username)
                set_access_cookies(response, access_token)
                return response
            return {"message": "Signup successful"}, 200
        return {"message": "User already exists"}, 409

@api_ns.route('/login')
class Login(Resource):
    @api_ns.expect(user_login_input_model)
    @api_ns.marshal_with(message_output_model, code=200, description="Login successful")
    @api_ns.marshal_with(message_output_model, code=401, description="Invalid credentials")
    def post(self):
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        user = UserManager.read(username)
        if user and argon2.check_password_hash(user.password, password):
            @after_this_request
            def set_access_cookie(response):
                access_token = create_access_token(identity=username)
                set_access_cookies(response, access_token)
                return response
            return {"message": "Login successful"}, 200
        return {"message": "Invalid credentials"}, 401

@api_ns.route('/logout')
class Logout(Resource):
    @api_ns.marshal_with(message_output_model, code=200, description="Logout successful")
    def post(self):
        @after_this_request
        def unset_access_cookie(response):
            unset_jwt_cookies(response)
            return response
        return {"message": "Logout successful"}, 200