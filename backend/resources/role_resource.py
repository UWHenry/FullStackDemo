from db_utils.role_manager import RoleManager
from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required
from .namespace_models import (
    api_ns, 
    message_output_model, 
    role_model, 
    role_input_model, 
    role_search_input_model, 
    role_search_output_model
)


# Role Read and Delete
@api_ns.route('/role/<string:rolename>')
class RoleResource(Resource):
    @api_ns.param('rolename', 'The rolename of the role to read', type='string', required=True)
    @api_ns.response(model=role_model, code=200, description="Role model")
    @api_ns.response(model=message_output_model, code=404, description="Role not found")
    @jwt_required()
    def get(self, rolename: str):
        result_role = RoleManager.read(rolename)
        if result_role:
            return result_role.as_dict(), 200
        return {"message": "Role not found"}, 404

    @api_ns.param('rolename', 'The rolename of the role to delete', type='string', required=True)
    @api_ns.marshal_with(message_output_model, code=200, description="Success")
    @api_ns.marshal_with(message_output_model, code=404, description="Role not found")
    @api_ns.marshal_with(message_output_model, code=500, description="Fail")
    @jwt_required()
    def delete(self, rolename: str):
        role = RoleManager.read(rolename)
        if role is None:
            return {"message": "Role not found"}, 404
        success = RoleManager.delete(rolename)
        if success:
            return {"message": "Success"}, 200
        return {"message": "Fail"}, 500

# Role Create and Update
@api_ns.route('/role')
class RoleUpdateResource(Resource):
    @api_ns.expect(role_input_model)
    @api_ns.marshal_with(message_output_model, code=200, description="Success")
    @api_ns.marshal_with(message_output_model, code=400, description="Invalid json body")
    @api_ns.marshal_with(message_output_model, code=409, description="Role already Exists")
    @jwt_required()
    def post(self):
        data = request.get_json()
        rolename = data.get("rolename", None)
        permission = data.get("permission", None)
        description = data.get("description", "")
        users = data.get("users", [])
        if not rolename or not permission:
            return {"message": "Invalid json body"}, 400
        new_role = RoleManager.create(rolename, permission, description, users)
        if new_role:
            return {"message": "Success"}, 200
        return {"message": "Role already Exists"}, 409

    @api_ns.expect(role_input_model)
    @api_ns.marshal_with(message_output_model, code=200, description="Success")
    @api_ns.marshal_with(message_output_model, code=400, description="Invalid json body")
    @api_ns.marshal_with(message_output_model, code=404, description="Role not found")
    @api_ns.marshal_with(message_output_model, code=500, description="Fail")
    @jwt_required()
    def put(self):
        data = request.get_json()
        rolename = data.get("rolename", None)
        permission = data.get("permission", None)
        description = data.get("description", None)
        users = data.get("users", None)
        if not rolename:
            return {"message": "Invalid rolename"}, 400
        if permission == "":
            return {"message": "Permission cannot be empty string"}, 400
        
        role = RoleManager.read(rolename)
        if role is None:
            return {"message": "Role not found"}, 404
        updated_role = RoleManager.update(rolename, role.version_id, permission, description, users)
        if updated_role:
            return {"message": "Success"}, 200
        return {"message": "Fail"}, 500

# Search Roles
@api_ns.route('/roles/search')
class RoleSearchResource(Resource):
    @api_ns.expect(role_search_input_model)
    @api_ns.marshal_with(role_search_output_model, code=200)
    @jwt_required()
    def post(self):
        data = request.get_json()
        page = data.get('page', 1)
        page_size = data.get('page_size', 10)
        if page < 1:
            page = 1
        if page_size < 1:
            page_size = 10

        sort_by = data.get('sort_by', 'rolename')
        reverse = data.get('reverse', False)
        search_rolename = data.get('search_rolename', None)
        search_permission = data.get('search_permission', None)
        search_description = data.get('search_description', None)
        role_list = RoleManager.search(
            page, page_size, sort_by, reverse, search_rolename, search_permission, search_description)
        role_list = [role.as_dict() for role in role_list]

        total_items = RoleManager.count()
        total_pages = (total_items + page_size - 1) // page_size
        return {"roles": role_list, "total_pages": total_pages}, 200

# List Roles
@api_ns.route('/roles')
class RoleListResource(Resource):
    @api_ns.marshal_list_with(role_model, code=200)
    @jwt_required()
    def get(self):
        role_list = RoleManager.list()
        role_list = [role.as_dict() for role in role_list]
        return role_list, 200