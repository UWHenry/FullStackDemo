from testing_env_setup import app
import time
from app import socketio

class TestAliveSocket:
    def _filter_responses(self, name, response):
        return list(filter(lambda x: x["name"] == name, response))
    
    def _get_response_messages(self, response):
        def get_event_message(event):
            if len(event["args"]) == 0:
                return None
            return event["args"][0]
        return list(map(lambda x: get_event_message(x), response))

    def test_receive(self):
        client = socketio.test_client(app)
        client.connect()
        time.sleep(3)
        response = client.get_received()
        response = self._filter_responses("alive_message", response)
        messages = self._get_response_messages(response)
        assert len(messages) == 1
        assert messages[0] == "is still alive?"
        client.disconnect()
    
    def test_disconnect(self):
        client = socketio.test_client(app)
        client.connect()
        time.sleep(6)
        response = client.get_received()
        disconnect_response = self._filter_responses("disconnect", response)
        response = self._filter_responses("alive_message", response)
        messages = self._get_response_messages(response)
        assert len(disconnect_response) == 1
        assert "Disconnecting due to inactivity!" in messages
        client.disconnect()
    
    def test_wrong_reply(self):
        client = socketio.test_client(app)
        client.connect()
        time.sleep(3)
        response = client.get_received()
        response = self._filter_responses("alive_message", response)
        messages = self._get_response_messages(response)
        if "is still alive?" in messages:
            client.emit("alive_message", "wrong reply")
        time.sleep(3)
        response = client.get_received()
        disconnect_response = self._filter_responses("disconnect", response)
        response = self._filter_responses("alive_message", response)
        messages = self._get_response_messages(response)
        assert len(disconnect_response) == 1
        assert "Disconnecting due to inactivity!" in messages
        client.disconnect()
    
    def test_reply(self):
        client = socketio.test_client(app)
        client.connect()
        time.sleep(3)
        response = client.get_received()
        response = self._filter_responses("alive_message", response)
        messages = self._get_response_messages(response)
        if "is still alive?" in messages:
            client.emit("alive_message", "alive")
        time.sleep(3)
        response = client.get_received()
        disconnect_response = self._filter_responses("disconnect", response)
        response = self._filter_responses("alive_message", response)
        messages = self._get_response_messages(response)
        assert len(disconnect_response) == 0
        assert "Disconnecting due to inactivity!" not in messages
        client.disconnect()