import os
import time
import secrets

from flask import Flask, request
from flask_restx import Api
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

from resources.db_testing_resource import db_testing_ns
from resources.csrf_resource import api_ns as csfr_ns
from resources.role_resource import api_ns as role_ns
from resources.user_resource import api_ns as user_ns
from db_utils.user_manager import argon2
from models import db


app = Flask(__name__)
api = Api(app, version='1.0', title='My API')
api.add_namespace(db_testing_ns)
api.add_namespace(csfr_ns)
api.add_namespace(role_ns)
api.add_namespace(user_ns)

app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600 # access token lifespan in seconds
app.config['WTF_CSRF_SSL_STRICT'] = False # avoids CSRF same origin policy check
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 
with app.app_context():
    db.create_all()


CORS(app, origins=["https://localhost:3000", "https://localhost:8443"], supports_credentials=True)
csrf = CSRFProtect(app)
jwt = JWTManager(app)
argon2.init_app(app)
socketio = SocketIO(app)


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
    socketio.run(app, port=8000, debug=True)