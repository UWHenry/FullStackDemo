from testing_env_setup import app, db, client
from db_utils.user_manager import UserManager
from db_utils.role_manager import RoleManager

class TestManyToMany:
    def _clean_up(self):
        with app.app_context():
            for user in UserManager.list():
                UserManager.delete(user)
            for role in RoleManager.list():
                RoleManager.delete(role)
            db.session.commit()

    def test_add(self, client):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            RoleManager.create("test_rolename", "read", "read permission", ["test_username"])
            UserManager.create("test_username2", "test_password", "test_address", ["test_rolename"])
            db.session.commit()
            user = UserManager.read("test_username")
            user2 = UserManager.read("test_username2")
            role = RoleManager.read("test_rolename")
            assert len(user.roles) == 1
            assert user.roles[0] == role
            assert len(user2.roles) == 1
            assert user2.roles[0] == role
            assert len(role.users) == 2
            assert role.users[0] == user
            assert role.users[1] == user2
        self._clean_up()   