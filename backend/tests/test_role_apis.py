from testing_env_setup import app, db, client
from db_utils.user_manager import UserManager
from db_utils.role_manager import RoleManager
from http.cookies import SimpleCookie

class TestRoleAPIs:
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
    
    def test_role_get_unauthorized(self, client):
        response = client.get("/api/role/test_rolename")
        assert response.status_code == 401
    
    def test_role_get_not_found(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/role/test_rolename")
        assert response.status_code == 404
        self._clean_up()
    
    def test_role_get(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        with app.app_context():
            RoleManager.create("test_rolename", "read", "read permission", [])
            db.session.commit()
        response = client.get("/api/role/test_rolename")
        assert response.status_code == 200
        assert response.get_json() == {"rolename": "test_rolename", "permission": "read", "description": "read permission", "users": []}
        self._clean_up()
        
    def test_role_put_unauthorized(self, client):
        response = client.put("/api/role/test_rolename", json={})
        assert response.status_code == 401
    
    def test_role_put_unauthorized_csrf(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.put("/api/role/test_rolename", json={})
        assert response.status_code == 401
        self._clean_up()

    def test_role_put_not_found(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.put("/api/role/test_rolename", headers={"X-CSRF-TOKEN": csrf_token}, json={})
        assert response.status_code == 404
        self._clean_up()
        
    def test_role_put_bad_request(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        with app.app_context():
            RoleManager.create("test_rolename", "read", "read permission", [])
            db.session.commit()
        csrf_token = self._get_csrf_cookie(response)
        response = client.put("/api/role/test_rolename", headers={"X-CSRF-TOKEN": csrf_token}, json={"permission": 123})
        assert response.status_code == 400
        self._clean_up()
        
    def test_role_put(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        with app.app_context():
            RoleManager.create("test_rolename", "read", "read permission", [])
            db.session.commit()
        csrf_token = self._get_csrf_cookie(response)
        response = client.put("/api/role/test_rolename", headers={"X-CSRF-TOKEN": csrf_token}, json={"permission": "write"})
        assert response.status_code == 200
        role = RoleManager.read("test_rolename")
        assert role is not None
        assert role.permission == "write"
        self._clean_up()
        
    def test_role_delete_unauthorized(self, client):
        response = client.delete("/api/role/test_rolename")
        assert response.status_code == 401
    
    def test_role_delete_not_found(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.delete("/api/role/test_rolename", headers={"X-CSRF-TOKEN": csrf_token})
        assert response.status_code == 404
        self._clean_up()
    
    def test_role_delete(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        with app.app_context():
            RoleManager.create("test_rolename", "read", "read permission", [])
            db.session.commit()
        csrf_token = self._get_csrf_cookie(response)
        response = client.delete("/api/role/test_rolename", headers={"X-CSRF-TOKEN": csrf_token})
        assert response.status_code == 200
        role = RoleManager.read("test_rolename")
        assert role is None
        self._clean_up()
    
    def test_role_post_unauthorized(self, client):
        response = client.post("/api/role", json={"rolename": "test_rolename", "permission": "read", "description": "read permission"})
        assert response.status_code == 401
    
    def test_role_post_unauthorized_csrf(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.post("/api/role", json={"rolename": "test_rolename", "permission": "read", "description": "read permission"})
        assert response.status_code == 401
        self._clean_up()

    def test_role_post_bad_request(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/role", headers={"X-CSRF-TOKEN": csrf_token}, json={"rolename": "test_rolename"})
        assert response.status_code == 400
        self._clean_up()
        
    def test_role_post_role_exists(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/role", 
                               headers={"X-CSRF-TOKEN": csrf_token},
                               json={"rolename": "test_rolename", "permission": "read", "description": "read permission"})
        response = client.post("/api/role", 
                               headers={"X-CSRF-TOKEN": csrf_token},
                               json={"rolename": "test_rolename", "permission": "read", "description": "read permission"})
        assert response.status_code == 409
        self._clean_up()
        
    def test_role_post(self, client):
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/role", 
                               headers={"X-CSRF-TOKEN": csrf_token},
                               json={"rolename": "test_rolename", "permission": "read", "description": "read permission"})
        assert response.status_code == 200
        role = RoleManager.read("test_rolename")
        assert role is not None
        self._clean_up()
    
    def test_role_search(self, client):
        with app.app_context():
            for i in range(9):
                RoleManager.create(f"test_rolename{i}", "read", "read permission", [])
            db.session.commit()
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        csrf_token = self._get_csrf_cookie(response)
        response = client.post("/api/roles/search",
                               headers={"X-CSRF-TOKEN": csrf_token},
                               json={"page": 1, "page_size": 5, "reverse": True})
        data = response.get_json()
        roles = data["roles"]
        total_pages = data["total_pages"]
        assert response.status_code == 200
        assert total_pages == 2
        assert roles[0]["rolename"] == "test_rolename8"
        assert roles[4]["rolename"] == "test_rolename4"
        self._clean_up()
    
    def test_role_list(self, client):
        with app.app_context():
            for i in range(9):
                RoleManager.create(f"test_rolename{i}", "read", "read permission", [])
            db.session.commit()
        response = client.post("/api/signup", json={"username": "test_username", "password": "test_password"})
        response = client.get("/api/roles")
        data = response.get_json()
        rolenames = set(map(lambda x: x["rolename"], data))
        assert response.status_code == 200
        assert rolenames == set([f"test_rolename{i}" for i in range(9)])
        self._clean_up()