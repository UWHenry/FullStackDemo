import os
import time
import secrets
from datetime import datetime, timedelta, timezone

from flask import Flask
from flask_restx import Api
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager, 
    get_jwt, 
    set_access_cookies, 
    get_jwt_identity, 
    create_access_token
)

from resources.authentication_resource import api_ns as auth_ns
from resources.db_testing_resource import db_testing_ns
from resources.csrf_resource import api_ns as csfr_ns
from resources.role_resource import api_ns as role_ns
from resources.user_resource import api_ns as user_ns
from db_utils.user_manager import argon2
from models import db


app = Flask(__name__)
api = Api(app, version='1.0', title='My API')
api.add_namespace(auth_ns)
api.add_namespace(db_testing_ns)
api.add_namespace(csfr_ns)
api.add_namespace(role_ns)
api.add_namespace(user_ns)

# Generate a 32-byte (256-bit) random key
app.config['SECRET_KEY'] = secrets.token_hex(32)
# manages json web token and csrf using cookies
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 
with app.app_context():
    db.create_all()

CORS(app, origins=["https://localhost:3000", "https://localhost:8443"], supports_credentials=True)
jwt = JWTManager(app)
argon2.init_app(app)
socketio = SocketIO(app)

# refresh jwt if it is going to expire within 30 minutes
@app.after_request
def refresh_expiring_jwts(response):
    try:
        exp_timestamp = get_jwt()["exp"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            set_access_cookies(response, access_token)
        return response
    except (RuntimeError, KeyError):
        return response

# web sockets
# last_client_message_time = {} 
# @socketio.on('connect')
# def handle_connect():
#     last_client_message_time[request.sid] = time.time()

# @socketio.on('disconnect')
# def handle_disconnect():
#     last_client_message_time.pop(request.sid)

# @socketio.on('message_from_frontend')
# def handle_message_from_frontend(message):
#     last_client_message_time[request.sid] = time.time()

# def send_alive_message():
#     while True:
#         socketio.sleep(60)
#         emit('message_from_backend', 'is still alive?')
        
# def check_client_activity():
#     while True:
#         socketio.sleep(60)
#         current_time = time.time()
#         for client_id, last_message_time in last_client_message_time.items():
#             if current_time - last_message_time > 180:
#                 socketio.disconnect(client_id)

# socketio.start_background_task(send_alive_message)
# socketio.start_background_task(check_client_activity)

if __name__ == '__main__':
    ssl_certificate = (
        "backend/certificates/certificate.crt",
        "backend/certificates/private.key"
    )
    socketio.run(app, port=8000, ssl_context=ssl_certificate, debug=True)