from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from models import db
from db_utils.role_manager import RoleManager
from .namespace_models import (
    api_ns,
    role_model, 
    role_create_input_model,
    role_update_input_model,
    role_search_input_model, 
    role_search_output_model
)


# Role Read, Update and Delete
@api_ns.route('/role/<string:rolename>')
class RoleResource(Resource):
    @api_ns.param('rolename', 'The rolename of the role to read', type='string', required=True)
    @api_ns.response(200, "Role model", role_model)
    @api_ns.response(401, "Unauthorized")
    @api_ns.response(404, "Role Not Found")
    @api_ns.doc(description='Get the role with the given rolename')
    @jwt_required()
    def get(self, rolename: str):
        role = RoleManager.read(rolename)
        if role:
            return role.as_dict(), 200
        return "Role Not Found", 404
    
    @api_ns.param('rolename', 'The rolename of the role to read', type='string', required=True)
    @api_ns.expect(role_update_input_model)
    @api_ns.response(200, 'Success')
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(401, "Unauthorized")
    @api_ns.response(404, 'Role Not Found')
    @api_ns.response(409, 'Optimistic Lock Conflict')
    @api_ns.response(500, 'Internal Server Error')
    @api_ns.doc(description='Update the role with the given rolename')
    @jwt_required()
    def put(self, rolename: str):
        data = request.get_json()
        permission = data.get("permission", None)
        description = data.get("description", None)
        users = data.get("users", None)
        try:
            role = RoleManager.read(rolename)
            if role:
                RoleManager.update(role, permission, description, users)
                db.session.commit()
                return "Success", 200
            return "Role Not Found", 404
        except StaleDataError:
            db.session.rollback()
            return "Optimistic Lock Conflict", 409
        except:
            db.session.rollback()
            return 'Internal Server Error', 500

    @api_ns.param('rolename', 'The rolename of the role to delete', type='string', required=True)
    @api_ns.response(200, "Success")
    @api_ns.response(401, "Unauthorized")
    @api_ns.response(404, "Role Not Found")
    @api_ns.response(409, 'Optimistic Lock Conflict')
    @api_ns.response(500, "Internal Server Error")
    @api_ns.doc(description='Delete the role with the given rolename')
    @jwt_required()
    def delete(self, rolename: str):
        try:
            role = RoleManager.read(rolename)
            if role:
                RoleManager.delete(role)
                db.session.commit()
                return "Success", 200
            return "Role Not Found", 404 
        except StaleDataError:
            db.session.rollback()
            return "Optimistic Lock Conflict", 409   
        except Exception:
            db.session.rollback()
            return "Internal Server Error", 500

# Role Create
@api_ns.route('/role')
class RoleCreateResource(Resource):
    @api_ns.expect(role_create_input_model)
    @api_ns.response(200, 'Success')
    @api_ns.response(400, 'Bad Request')
    @api_ns.response(401, "Unauthorized")
    @api_ns.response(409, 'Role Already Exists')
    @api_ns.response(500, 'Internal Server Error')
    @api_ns.doc(description='Create a new role')
    @jwt_required()
    def post(self):
        data = request.get_json()
        rolename = data.get("rolename")
        permission = data.get("permission")
        description = data.get("description", "")
        users = data.get("users", [])
        try:
            RoleManager.create(rolename, permission, description, users)
            db.session.commit()
            return "Success", 200
        except IntegrityError:
            db.session.rollback()
            return "Role Already Exists", 409
        except:
            db.session.rollback()
            return 'Internal Server Error', 500

# Search Roles
@api_ns.route('/roles/search')
class RoleSearchResource(Resource):
    @api_ns.expect(role_search_input_model)
    @api_ns.response(401, "Unauthorized")
    @api_ns.marshal_with(role_search_output_model, code=200)
    @api_ns.doc(description='Search roles')
    @jwt_required()
    def post(self):
        data = request.get_json()
        page = data.get('page', 1)
        page_size = data.get('page_size', 1)
        sort_by = data.get('sort_by', 'rolename')
        reverse = data.get('reverse', False)
        search_rolename = data.get('search_rolename', None)
        search_permission = data.get('search_permission', None)
        search_description = data.get('search_description', None)

        role_list, total_pages = RoleManager.search(
            page, page_size, sort_by, reverse, search_rolename, search_permission, search_description)
        role_list = [role.as_dict() for role in role_list]
        return {"roles": role_list, "total_pages": total_pages}, 200

# List Roles
@api_ns.route('/roles')
class RoleListResource(Resource):
    @api_ns.response(401, "Unauthorized")
    @api_ns.marshal_list_with(role_model, code=200)
    @api_ns.doc(description='List all roles')
    @jwt_required()
    def get(self):
        role_list = RoleManager.list()
        role_list = [role.as_dict() for role in role_list]
        return role_list, 200