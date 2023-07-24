from db_utils import role_manager
from flask import request
from flask_restx  import Resource, fields
from flask_jwt_extended import jwt_required
from . import ns

# models for swagger
user_model = ns.model("Role's Users Field", {
    'username': fields.String(required=True, description='The user username'),
    'address': fields.String(required=True, description='The user address')
})
role_model = ns.model('Role Model', {
    'rolename': fields.String(required=True, description='The role name'),
    'permission': fields.String(required=True, description='The role permission'),
    'description': fields.String(required=True, description='The role description'),
    'users':  fields.List(fields.Nested(user_model), required=True, description='List of role users')
})
role_input = ns.model('Role Create & Update Input', {
    'rolename': fields.String(required=True, description='The role name'),
    'permission': fields.String(required=True, description='The role permission'),
    'description': fields.String(required=True, description='The role description')
})
role_list_input = ns.model('Role List Input', {
    "page": fields.Integer(required=False),
    "page_size": fields.Integer(required=False),
    "sort_by": fields.String(required=False),
    "reverse": fields.String(required=False),
    "search_rolename": fields.String(required=False),
    "search_permission": fields.String(required=False),
    "search_description": fields.String(required=False)
})

roles = role_manager.RoleManager
    
# Role Read and Delete
@ns.route('/role/<string:rolename>')
class RoleResource(Resource):
    @ns.param('rolename', 'The rolename of the role to read', type='string', required=True)
    @ns.marshal_with(role_model, code=200)
    @ns.marshal_with(None, code=404, description="Role not found")
    @jwt_required()
    def get(self, rolename: str):
        result_role = roles.read(rolename)
        if result_role:
            return result_role.as_dict(), 200
        return {"message": "Role not found"}, 404
    
    @ns.marshal_with(None, code=200, description="Success")
    @ns.marshal_with(None, code=404, description="Role not found")
    @ns.marshal_with(None, code=500, description="Fail")
    @jwt_required()
    def delete(self, rolename: str):
        message = roles.delete(rolename)
        if message == "Success":
            return {"message": "Success"}, 200
        if message == "Role not found":
            return {"message": "Role not found"}, 404
        return {"message": "Fail"}, 500

# Roles Create and Update
@ns.route('/role')
class RoleUpdateResource(Resource):
    @ns.expect(role_input)
    @ns.marshal_with(None, code=200, description="Success")
    @ns.marshal_with(None, code=400, description="Invalid json body")
    @ns.marshal_with(None, code=409, description="Role already Exists")
    @jwt_required()
    def post(self):
        data = request.get_json()
        rolename = data.get("rolename", None)
        permission = data.get("permission", None)
        description = data.get("description", None)
        if not rolename or not permission:
            return {"message": "Invalid json body"}, 400
        new_role = roles.create(rolename, permission, description)
        if new_role:
            return {"message": "Success"}, 200
        return {"message": "Role already Exists"}, 409
        
        
    @ns.expect(role_input)
    @ns.marshal_with(None, code=200, description="Success")
    @ns.marshal_with(None, code=400, description="Invalid json body")
    @ns.marshal_with(None, code=404, description="Role not found")
    @ns.marshal_with(None, code=500, description="Fail")
    @jwt_required()
    def put(self):
        data = request.get_json()
        rolename = data.get("rolename", None)
        permission = data.get("permission", None)
        description = data.get("description", None)
        if not rolename:
            return {"message": "Invalid rolename"}, 400
        if permission == "":
            return {"message": "Permission cannot be empty string"}, 400
        message = roles.update(rolename, permission, description)
        if message == "Success":
            return {"message": "Success"}, 200
        if message == "Role not found":
            return {"message": "Role not found"}, 404
        return {"message": "Fail"}, 500

# List Roles
@ns.route('/roles')
class RoleListResource(Resource):
    @ns.marshal_list_with(role_model, code=200)
    @jwt_required()
    def get(self):
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        sort_by = request.args.get('sort_by', 'rolename')
        reverse = request.args.get('reverse', "false") == "true"
        search_rolename = request.args.get('search_rolename', None)
        search_permission = request.args.get('search_permission', None)
        search_description = request.args.get('search_description', None)
        role_list = roles.list(page, page_size, sort_by, reverse, search_rolename, search_permission, search_description)
        role_list = [role.as_dict() for role in role_list]
        return role_list, 200
