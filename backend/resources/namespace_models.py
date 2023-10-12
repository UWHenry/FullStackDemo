from flask_restx  import Namespace, fields

api_ns = Namespace('api')

# testing models
test_result = api_ns.model('TestResult', {
    'process_id': fields.Integer,
    'update_result': fields.String
})

# user related models
user_role_model = api_ns.model("UserRole", {
    'rolename': fields.String(required=True, description='The role name'),
    'permission': fields.String(required=True, description='The role permission'),
    'description': fields.String(required=True, description='The role description')
})
user_model = api_ns.model('User', {
    'username': fields.String(required=True, description='The user username'),
    'address': fields.String(required=True, description='The user address'),
    'roles': fields.List(fields.Nested(user_role_model), required=True, description='List of user roles')
})
user_create_input_model = api_ns.model('UserSignupInput', {
    'username': fields.String(required=True, min_length=1),
    'password': fields.String(required=True, min_length=1),
    'address': fields.String,
    'roles': fields.List(fields.String, description="rolenames")
})
user_login_input_model = api_ns.model('UserLoginInput', {
    'username': fields.String(required=True, min_length=1),
    'password': fields.String(required=True, min_length=1)
})
user_update_input_model = api_ns.model('UserUpdateInput', {
    'password': fields.String,
    'address': fields.String,
    'roles': fields.List(fields.String, description="rolenames")
})
user_search_input_model = api_ns.model('UserSearchInput', {
    "page": fields.Integer(required=True, min=1),
    "page_size": fields.Integer(required=True, min=1),
    "sort_by": fields.String(enum=["username", "address"]),
    "reverse": fields.Boolean,
    "search_username": fields.String,
    "search_address": fields.String
})
user_search_output_model = api_ns.model('UserSearchOutput', {
    "users": fields.List(fields.Nested(user_model)),
    "total_pages": fields.Integer
})

# role related models
role_user_model = api_ns.model("RoleUser", {
    'username': fields.String(required=True, description='The user username'),
    'address': fields.String(required=True, description='The user address')
})
role_model = api_ns.model('Role', {
    'rolename': fields.String(required=True, description='The role name'),
    'permission': fields.String(required=True, description='The role permission'),
    'description': fields.String(required=True, description='The role description'),
    'users':  fields.List(fields.Nested(role_user_model), required=True, description='List of role users')
})
role_create_input_model = api_ns.model('RoleCreateInput', {
    'rolename': fields.String(required=True, min_length=1),
    'permission': fields.String(required=True, min_length=1),
    'description': fields.String,
    'users': fields.List(fields.String, description="usernames")
})
role_update_input_model = api_ns.model('RoleUpdateInput', {
    'permission': fields.String(min_length=1),
    'description': fields.String,
    'users': fields.List(fields.String, description="usernames")
})
role_search_input_model = api_ns.model('RoleSearchInput', {
    "page": fields.Integer(required=True, min=1),
    "page_size": fields.Integer(required=True, min=1),
    "sort_by": fields.String(enum=["rolename", "permission", "description"]),
    "reverse": fields.Boolean,
    "search_rolename": fields.String,
    "search_permission": fields.String,
    "search_description": fields.String
})
role_search_output_model = api_ns.model('RoleSearchOutput', {
    "roles": fields.List(fields.Nested(role_model)),
    "total_pages": fields.Integer
})