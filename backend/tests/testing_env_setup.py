import sys
import os

# Add the parent directory to sys.path
current_dir = os.path.dirname(__file__)
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# set up environment variables
os.environ['DATABASE_URL'] = "sqlite:///test.db"
os.environ['CORS_ORIGINS'] = ""

from client_alive_socket import SETTINGS
SETTINGS["IS_ALIVE_FREQUENCY"] = 2
SETTINGS["KEEP_ALIVE_TIME"] = 3

import pytest
from app import app, db

# pytest set up and tear down resources
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

