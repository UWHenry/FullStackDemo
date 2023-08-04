from flask_restx import Resource
from flask_wtf.csrf import generate_csrf
from .namespace_models import api_ns, csrf_token_model


@api_ns.route('/get_csrf_token')
class CSRFTokenResource(Resource):
    @api_ns.marshal_with(csrf_token_model, code=200, description="Return CSRF token")
    def get(self):
        csrf_token = generate_csrf()
        return {'csrf_token': csrf_token}, 200
