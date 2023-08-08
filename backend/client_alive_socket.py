import threading
import time
from flask_socketio import SocketIO, disconnect
from flask import request


socketio = SocketIO()
client_connections = {}
client_connections_lock = threading.Lock()
IS_ALIVE_FREQUENCY = 60
KEEP_ALIVE_TIME = 180

@socketio.on('connect')
def handle_connect():
    client_connections[request.sid] = time.time()

@socketio.on('disconnect')
def handle_disconnect():
    disconnect(request.sid)
    with client_connections_lock:
        client_connections.pop(request.sid)

@socketio.on('alive_message')
def handle_message(message):
    if message == "alive":
        with client_connections_lock:
            client_connections[request.sid] = time.time()

def send_alive_message():
    while True:
        socketio.sleep(IS_ALIVE_FREQUENCY)
        socketio.emit('alive_message', 'is still alive?')
        
def check_client_activity():
    while True:
        socketio.sleep(IS_ALIVE_FREQUENCY)
        current_time = time.time()
        with client_connections_lock:
            for client_id, last_message_time in client_connections.items():
                if current_time - last_message_time > KEEP_ALIVE_TIME:
                    socketio.emit('alive_message', data='Disconnecting due to inactivity!', to=client_id)
                    socketio.sleep(1)
                    socketio.emit('disconnect', to=client_id)