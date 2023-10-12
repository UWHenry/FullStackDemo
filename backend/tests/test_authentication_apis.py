from testing_env_setup import app, db, client
from db_utils.user_manager import UserManager
from db_utils.role_manager import RoleManager

class Template:
    def _clean_up(self):
        with app.app_context():
            for user in UserManager.list():
                UserManager.delete(user)
            for role in RoleManager.list():
                RoleManager.delete(role)
            db.session.commit()

class TestSignUpAPIs(Template):    
    def test_signup_bad_request(self, client):
        response = client.post("/api/signup", json={"username": "test_username"})
        assert response.status_code == 400

    def test_signup_user_already_exist(self, client):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            db.session.commit()
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        assert response.status_code == 409
        self._clean_up()

    def test_signup(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        with app.app_context():
            user = UserManager.read("test_username")
        assert response.status_code == 200
        assert user is not None
        self._clean_up()
        
class TestLoginAPIs(Template):
    def test_login_invalid_credentials(self, client):
        response = client.post("/api/login", json={"username": "test_username", "password": "test_password"})
        assert response.status_code == 401
    
    def test_login_bad_request(self, client):
        response = client.post("/api/login", json={"username": "test_username"})
        assert response.status_code == 400
    
    def test_login(self, client):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            db.session.commit()
        response = client.post("/api/login", json={"username": "test_username", "password": "test_password"})
        assert response.status_code == 200
        self._clean_up()
    
class TestCheckAuthAPI(Template):
    def test_check_auth_unauthorized(self, client):
        response = client.get("/api/check-auth")
        assert response.status_code == 401

    def test_check_auth_signup(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/check-auth")
        assert response.status_code == 200
        self._clean_up()
    
    def test_check_auth_login(self, client):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            db.session.commit()
        response = client.post("/api/login", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/check-auth")
        assert response.status_code == 200
        self._clean_up()

class TestLogoutAPI(Template):
    def test_logout(self, client):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            db.session.commit()
        client.post("/api/login", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/check-auth")
        assert response.status_code == 200
        client.post("/api/logout")
        response = client.get("/api/check-auth")
        assert response.status_code == 401
        self._clean_up()