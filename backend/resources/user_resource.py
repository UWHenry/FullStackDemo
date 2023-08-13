from db_utils.user_manager import UserManager
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from models import db
from .namespace_models import (
    api_ns,
    user_create_input_model,
    user_update_input_model,
    user_search_input_model,
    user_search_output_model,
    user_model
)

# User Read, Update, Delete
@api_ns.route('/user/<string:username>')
class UserResource(Resource):
    @api_ns.param('username', 'The username of the user to read', type='string', required=True)
    @api_ns.response(200, "User model", user_model)
    @api_ns.response(404, "User not found")
    @api_ns.doc(description='Get the user with the given username')
    @jwt_required()
    def get(self, username: str):
        user = UserManager.read(username)
        if user:
            return user.as_dict(), 200
        return "User not found", 404

    @api_ns.param('username', 'The username of the user to update', type='string', required=True)
    @api_ns.expect(user_update_input_model)
    @api_ns.response(200, 'Success')
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(404, 'User Not Found')
    @api_ns.response(409, 'Optimistic Lock Conflict')
    @api_ns.response(500, 'Internal Server Error')
    @api_ns.doc(description='Update the user with the given username')
    @jwt_required()
    def put(self, username: str):
        data = request.get_json()
        password = data.get("password", None)
        address = data.get("address", None)
        roles = data.get("roles", None)
        try:
            user = UserManager.read(username)
            if user:
                UserManager.update(user, password, address, roles)
                db.session.commit()
                return "Success", 200
            return "User Not Found", 404
        except StaleDataError:
            db.session.rollback()
            return "Optimistic Lock Conflict", 409
        except:
            db.session.rollback()
            return 'Internal Server Error', 500

    @api_ns.param('username', 'The username of the user to delete', type='string', required=True)
    @api_ns.response(200, "Success")
    @api_ns.response(404, "User Not Found")
    @api_ns.response(409, 'Optimistic Lock Conflict')
    @api_ns.response(500, "Internal Server Error")
    @api_ns.doc(description='Delete the user with the given username')
    @jwt_required()
    def delete(self, username: str):
        try:
            user = UserManager.read(username)
            if user:
                UserManager.delete(user)
                db.session.commit()
                return "Success", 200
            return "User Not Found", 404 
        except StaleDataError:
            db.session.rollback()
            return "Optimistic Lock Conflict", 409   
        except Exception:
            db.session.rollback()
            return "Internal Server Error", 500

@api_ns.route('/user')
class UserCreateResource(Resource):
    @api_ns.expect(user_create_input_model)
    @api_ns.response(200, 'Success')
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(409, 'User Already Exists')
    @api_ns.response(500, 'Internal Server Error')
    @api_ns.doc(description='Create a new user')
    @jwt_required()
    def post(self):
        data = request.get_json()
        try:
            create_user(data)
            return "Success", 200
        except IntegrityError:
            db.session.rollback()
            return "User Already Exists", 409
        except:
            db.session.rollback()
            return 'Internal Server Error', 500
    
def create_user(data):
    """
    Throws sqlalchemy.exc.IntegrityError and possible some other errors
    """
    username = data.get("username")
    password = data.get("password")
    address = data.get("address", "")
    roles = data.get("roles", [])
    UserManager.create(username, password, address, roles)
    db.session.commit()

# Search Users
@api_ns.route('/users/search')
class UserSearchResource(Resource):
    @api_ns.expect(user_search_input_model)
    @api_ns.marshal_list_with(user_search_output_model, code=200)
    @api_ns.doc(description='Search users')
    @jwt_required()
    def post(self):
        data = request.get_json()
        page = data.get('page', 1)
        page_size = data.get('page_size', 1)
        sort_by = data.get('sort_by', 'username')
        reverse = data.get('reverse', False)
        search_username = data.get('search_username', None)
        search_address = data.get('search_address', None)

        user_list, total_pages = UserManager.search(
            page, page_size, sort_by, reverse, search_username, search_address)
        user_list = [user.as_dict() for user in user_list]
        return {"users": user_list, "total_pages": total_pages}, 200

# List Users
@api_ns.route('/users')
class UserListResource(Resource):
    @api_ns.marshal_list_with(user_model, code=200)
    @api_ns.doc(description='List all users')
    @jwt_required()
    def get(self):
        user_list = UserManager.list()
        user_list = [user.as_dict() for user in user_list]
        return user_list, 200