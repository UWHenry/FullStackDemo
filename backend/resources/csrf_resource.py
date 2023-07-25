from flask_restx  import Resource, fields
from flask import session
from . import ns
from flask_wtf.csrf import generate_csrf

csrf_model = ns.model("CSRF Token API Output", {
    'csrf_token': fields.String(required=True, description='The role name')
})

@ns.route('/get_csrf_token')
class CSRFTokenResource(Resource):
    @ns.marshal_with(csrf_model, code=200, description="Return CSRF token if exists")
    def get(self):
        csrf_token = session.get('csrf_token')
        if not csrf_token:
            csrf_token = generate_csrf()
            session['csrf_token'] = csrf_token
        return {'csrf_token': csrf_token}, 200