from testing_env_setup import app, db
from db_utils.user_manager import UserManager
from db_utils.role_manager import RoleManager
from models.user import User
from models.role import Role

class TestUserManager:
    def _clean_up(self):
        with app.app_context():
            for user in User.query.all():
                db.session.delete(user)
            for role in Role.query.all():
                db.session.delete(role)
            db.session.commit()

    def test_create(self):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            db.session.commit()
            assert db.session.get(User, "test_username") is not None
        self._clean_up()

    def test_read(self):
        with app.app_context():
            new_user = User(
                username="test_username",
                password="test_password",
                address="test_address"
            )
            db.session.add(new_user)
            db.session.commit()
            user = UserManager.read("test_username")
            assert user is not None
            assert user.username == "test_username"
        self._clean_up()
    
    def test_update(self):
        with app.app_context():
            new_user = User(
                username="test_username",
                password="test_password",
                address="test_address"
            )
            db.session.add(new_user)
            db.session.commit()
            user = db.session.get(User, "test_username")
            UserManager.update(user, None, "test_address2", None)
            db.session.commit()
            user = db.session.get(User, "test_username")
            assert user.address == "test_address2"
        self._clean_up()
    
    def test_search(self):
        with app.app_context():
            for i in range(9):
                new_user = User(
                    username=f"test_username{i}",
                    password="test_password",
                    address="test_address"
                )
                db.session.add(new_user)
            db.session.commit()
            users, total_pages =  UserManager.search(2, 5, "username", False)
            assert len(users) == 4
            assert total_pages == 2
            assert users[0].username == "test_username5"
        self._clean_up()
    
    def test_list(self):
        with app.app_context():
            for i in range(9):
                new_user = User(
                    username=f"test_username{i}",
                    password="test_password",
                    address="test_address"
                )
                db.session.add(new_user)
            db.session.commit()
            users = UserManager.list()
            assert len(users) == 9
            assert users[0].username == "test_username0"
            assert users[-1].username == "test_username8"
        self._clean_up()

    def test_delete(self):
        with app.app_context():
            new_user = User(
                username="test_username",
                password="test_password",
                address="test_address"
            )
            db.session.add(new_user)
            db.session.commit()
            user = db.session.get(User, "test_username")
            UserManager.delete(user)
            db.session.commit()
            assert len(User.query.all()) == 0
        self._clean_up()

class TestRoleManager:
    def _clean_up(self):
        with app.app_context():
            for user in User.query.all():
                db.session.delete(user)
            for role in Role.query.all():
                db.session.delete(role)
            db.session.commit()

    def test_create(self):
        with app.app_context():
            RoleManager.create("test_rolename", "read", "have permission to read files", [])
            db.session.commit()
            assert db.session.get(Role, "test_rolename") is not None
        self._clean_up()

    def test_read(self):
        with app.app_context():
            new_role = Role(
                rolename="test_rolename",
                permission="read",
                description="have permission to read files"
            )
            db.session.add(new_role)
            db.session.commit()
            role = RoleManager.read("test_rolename")
            assert role is not None
            assert role.rolename == "test_rolename"
        self._clean_up()
    
    def test_update(self):
        with app.app_context():
            new_role = Role(
                rolename="test_rolename",
                permission="read",
                description="have permission to read files"
            )
            db.session.add(new_role)
            db.session.commit()
            role = db.session.get(Role, "test_rolename")
            RoleManager.update(role, None, "have read permission", None)
            db.session.commit()
            role = db.session.get(Role, "test_rolename")
            assert role.description == "have read permission"
        self._clean_up()
    
    def test_search(self):
        with app.app_context():
            for i in range(9):
                new_role = Role(
                    rolename=f"test_rolename{i}",
                    permission="read",
                    description="have permission to read files"
                )
                db.session.add(new_role)
            db.session.commit()
            roles, total_pages =  RoleManager.search(2, 5, "rolename", False)
            assert len(roles) == 4
            assert total_pages == 2
            assert roles[0].rolename == "test_rolename5"
        self._clean_up()
    
    def test_list(self):
        with app.app_context():
            for i in range(9):
                new_role = Role(
                    rolename=f"test_rolename{i}",
                    permission="read",
                    description="have permission to read files"
                )
                db.session.add(new_role)
            db.session.commit()
            roles = RoleManager.list()
            assert len(roles) == 9
            assert roles[0].rolename == "test_rolename0"
            assert roles[-1].rolename == "test_rolename8"
        self._clean_up()

    def test_delete(self):
        with app.app_context():
            new_role = Role(
                rolename="test_rolename",
                permission="read",
                description="have permission to read files"
            )
            db.session.add(new_role)
            db.session.commit()
            role = db.session.get(Role, "test_rolename")
            RoleManager.delete(role)
            db.session.commit()
            assert len(Role.query.all()) == 0
        self._clean_up()