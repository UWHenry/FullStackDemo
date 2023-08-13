from flask import request, after_this_request
from flask_restx import Resource
from flask_jwt_extended import create_access_token, unset_jwt_cookies, set_access_cookies
from sqlalchemy.exc import IntegrityError
from db_utils.user_manager import UserManager, argon2
from .namespace_models import (
    api_ns,
    user_create_input_model,
    user_login_input_model
)
from .user_resource import create_user
from models import db


@api_ns.route('/signup')
class SignUp(Resource):
    @api_ns.expect(user_create_input_model)
    @api_ns.response(200, 'Success')
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(409, 'User Already Exists')
    @api_ns.response(500, 'Internal Server Error')
    @api_ns.doc(description='Signup')
    def post(self):
        data = request.get_json()
        username = data.get("username")
        try:
            create_user(data)
            @after_this_request
            def set_access_cookie(response):
                access_token = create_access_token(identity=username)
                set_access_cookies(response, access_token)
                return response
            return "Success", 200
        except IntegrityError:
            db.session.rollback()
            return "User Already Exists", 409
        except:
            db.session.rollback()
            return 'Internal Server Error', 500

@api_ns.route('/login')
class Login(Resource):
    @api_ns.expect(user_login_input_model)
    @api_ns.response(200, 'Success')
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(401, 'Invalid Credentials')
    @api_ns.doc(description='Login')
    def post(self):
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = UserManager.read(username)
        if user and argon2.check_password_hash(user.password, password):
            @after_this_request
            def set_access_cookie(response):
                access_token = create_access_token(identity=username)
                set_access_cookies(response, access_token)
                return response
            return "Success", 200
        return "Invalid Credentials", 401

@api_ns.route('/logout')
class Logout(Resource):
    @api_ns.response(200, 'Success')
    @api_ns.doc(description='Logout')
    def post(self):
        @after_this_request
        def unset_access_cookie(response):
            unset_jwt_cookies(response)
            return response
        return "Success", 200