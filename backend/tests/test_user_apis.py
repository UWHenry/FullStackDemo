from testing_env_setup import app, db, client
from db_utils.user_manager import UserManager
from db_utils.role_manager import RoleManager
from http.cookies import SimpleCookie

class TestUserAPIs:
    def _clean_up(self):
        with app.app_context():
            for user in UserManager.list():
                UserManager.delete(user)
            for role in RoleManager.list():
                RoleManager.delete(role)
            db.session.commit()
    
    def _get_csrf_cookie(self, response):
        set_cookie_headers = response.headers.getlist('Set-Cookie')
        for set_cookie_header in set_cookie_headers:
            if "csrf_access_token" in set_cookie_header:
                cookies = SimpleCookie()
                cookies.load(set_cookie_header)
                csrf_access_token = cookies.get('csrf_access_token').value
                return csrf_access_token
        return None
    
    def test_user_get_unauthorized(self, client):
        response = client.get("/api/user/test_username")
        assert response.status_code == 401
    
    def test_user_get_not_found(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/user/username_nonexist")
        assert response.status_code == 404
        self._clean_up()
    
    def test_user_get(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/user/test_username")
        assert response.status_code == 200
        assert response.get_json() == {"username": "test_username", "address": "", "roles": []}
        self._clean_up()
        
    def test_user_put_unauthorized(self, client):
        response = client.put("/api/user/test_username", json={})
        assert response.status_code == 401
    
    def test_user_put_unauthorized_csrf(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.put("/api/user/username_nonexist", json={})
        assert response.status_code == 401
        self._clean_up()

    def test_user_put_not_found(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.put("/api/user/username_nonexist", headers={"X-CSRF-TOKEN": csrf_token}, json={})
        assert response.status_code == 404
        self._clean_up()
        
    def test_user_put_bad_request(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.put("/api/user/test_username", headers={"X-CSRF-TOKEN": csrf_token}, json={"password": 123})
        assert response.status_code == 400
        self._clean_up()
        
    def test_user_put(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.put("/api/user/test_username", headers={"X-CSRF-TOKEN": csrf_token}, json={"address": "test_address_2"})
        assert response.status_code == 200
        user = UserManager.read("test_username")
        assert user is not None
        assert user.address == "test_address_2"
        self._clean_up()
        
    def test_user_delete_unauthorized(self, client):
        response = client.delete("/api/user/test_username")
        assert response.status_code == 401
    
    def test_user_delete_not_found(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.delete("/api/user/username_nonexist", headers={"X-CSRF-TOKEN": csrf_token})
        assert response.status_code == 404
        self._clean_up()
    
    def test_user_delete(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        user = UserManager.read("test_username")
        assert user.username == "test_username"
        response = client.delete("/api/user/test_username", headers={"X-CSRF-TOKEN": csrf_token})
        assert response.status_code == 200
        user = UserManager.read("test_username")
        assert user is None
        self._clean_up()
    
    def test_user_post_unauthorized(self, client):
        response = client.post("/api/user", json={"username": "test_username2", "password": "test_password2", "address": "test_address"})
        assert response.status_code == 401
    
    def test_user_post_unauthorized_csrf(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.post("/api/user", json={"username": "test_username2", "password": "test_password2", "address": "test_address"})
        assert response.status_code == 401
        self._clean_up()

    def test_user_post_bad_request(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/user", headers={"X-CSRF-TOKEN": csrf_token}, json={"username": "test_username2"})
        assert response.status_code == 400
        self._clean_up()
        
    def test_user_post_user_exists(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/user", headers={"X-CSRF-TOKEN": csrf_token}, json={"username": "test_username", "password": "test_password2"})
        assert response.status_code == 409
        self._clean_up()
        
    def test_user_post(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/user",
                               headers={"X-CSRF-TOKEN": csrf_token},
                               json={"username": "test_username2", "password": "test_password2", "address": "test_address"})
        assert response.status_code == 200
        user = UserManager.read("test_username2")
        assert user is not None
        self._clean_up()
    
    def test_user_search(self, client):
        with app.app_context():
            for i in range(9):
                UserManager.create(f"test_username{i}", "test_password", "test_address", [])
            db.session.commit()
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/users/search",
                               headers={"X-CSRF-TOKEN": csrf_token},
                               json={"page": 1, "page_size": 5, "reverse": True})
        data = response.get_json()
        users = data["users"]
        total_pages = data["total_pages"]
        assert response.status_code == 200
        assert total_pages == 2
        assert users[0]["username"] == "test_username8"
        assert users[4]["username"] == "test_username4"
        self._clean_up()
    
    def test_user_list(self, client):
        with app.app_context():
            for i in range(9):
                UserManager.create(f"test_username{i}", "test_password", "test_address", [])
            db.session.commit()
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/users")
        data = response.get_json()
        usernames = set(map(lambda x: x["username"], data))
        assert response.status_code == 200
        assert usernames == set(["test_username"] + [f"test_username{i}" for i in range(9)])
        self._clean_up()