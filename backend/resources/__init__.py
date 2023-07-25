from flask_restx  import Namespace, fields

ns = Namespace('api')

message_model = ns.model('Text Message Output', {
    "message": fields.String(required=True)
})