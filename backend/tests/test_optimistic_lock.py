from testing_env_setup import app, db
from db_utils.user_manager import UserManager
from db_utils.role_manager import RoleManager
from sqlalchemy.orm.exc import StaleDataError
import multiprocessing

class TestOptimisticLock:
    def _clean_up(self):
        with app.app_context():
            for user in UserManager.list():
                UserManager.delete(user)
            for role in RoleManager.list():
                RoleManager.delete(role)
            db.session.commit()

    def _update_user_address(self, address):
        with app.app_context():
            try:
                user = UserManager.read("test_username")
                UserManager.update(user, None, address, None)
                db.session.commit()
            except StaleDataError:
                db.session.rollback()
                return "Optimistic Lock Conflict"
        return ""
        
    def test_user_update_optimistic_lock(self):
        with app.app_context():
            UserManager.create("test_username", "test_password", "test_address", [])
            db.session.commit()
        data = [f"test_adress_{i}" for i in range(10)]
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.map(self._update_user_address, data)
        assert "Optimistic Lock Conflict" in results
        self._clean_up()
        
    def _update_role_description(self, description):
        with app.app_context():
            try:
                role = RoleManager.read("test_rolename")
                RoleManager.update(role, None, description, None)
                db.session.commit()
            except StaleDataError:
                db.session.rollback()
                return "Optimistic Lock Conflict"
        return ""

    def test_role_update_optimistic_lock(self):
        with app.app_context():
            RoleManager.create("test_rolename", "read", "read permission", [])
            db.session.commit()
        data = [f"read permission {i}" for i in range(10)]
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.map(self._update_role_description, data)
        assert "Optimistic Lock Conflict" in results
        self._clean_up()