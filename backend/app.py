import os
import time

from flask import Flask, request
from flask_restx import Api
from flask_socketio import SocketIO, emit

from resources.user_resource import ns as user_ns
from resources.role_resource import ns as role_ns
from resources.csrf_resource import ns as csrf_ns
from resources.db_testing_resource import db_testing_ns

from flask_jwt_extended import JWTManager
from flask_wtf.csrf import CSRFProtect

from models import db
from db_utils import argon2, user_manager


app = Flask(__name__)
api = Api(app)


app.config['SECRET_KEY'] = 'uFTuxjpGQxU8EsfcVPcTJfzqwG1CrjWk'
csrf = CSRFProtect(app)
jwt = JWTManager(app)
argon2.init_app(app)
socketio = SocketIO(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://my_user:my_password@localhost:5432/my_db"

db.init_app(app) 
with app.app_context():
    db.create_all()

api.add_namespace(user_ns)
api.add_namespace(role_ns)
api.add_namespace(csrf_ns)
api.add_namespace(db_testing_ns)
 

# web sockets
last_client_message_time = {} 
@socketio.on('connect')
def handle_connect():
    last_client_message_time[request.sid] = time.time()

@socketio.on('disconnect')
def handle_disconnect():
    last_client_message_time.pop(request.sid)

@socketio.on('message_from_frontend')
def handle_message_from_frontend(message):
    last_client_message_time[request.sid] = time.time()

def send_alive_message():
    while True:
        socketio.sleep(60)
        emit('message_from_backend', 'is still alive?')
        
def check_client_activity():
    while True:
        socketio.sleep(60)
        current_time = time.time()
        for client_id, last_message_time in last_client_message_time.items():
            if current_time - last_message_time > 180:
                socketio.disconnect(client_id)

# socketio.start_background_task(send_alive_message)
# socketio.start_background_task(check_client_activity)

if __name__ == '__main__':
    socketio.run(app, debug=True)