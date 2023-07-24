from flask_restx  import Resource
from flask_jwt_extended import jwt_required
from flask import session
from . import ns

@ns.route('/get_csrf_token')
class CSRFTokenResource(Resource):
    @ns.marshal_with(None, code=200, description="Return CSRF token if exists")
    @jwt_required()
    def get(self):
        csrf_token = session.get('csrf_token')
        return {'csrf_token': csrf_token}, 200