import multiprocessing
from typing import Tuple

from flask_restx import Resource
from flask import Flask

from db_utils.role_manager import RoleManager
from namespace_models import db_testing_ns, optimistic_lock_result
from models import db


def test_optimistic_lock(rolename: str, index: int, version_id: int) -> Tuple[int, str]:
    """
    Initializes a new flask app, setup database connections, and update the database.
    version_id is retrived prior to process creation to simulate resource competition.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://my_user:my_password@localhost:5432/my_db"
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    db.init_app(app)
    with app.app_context():
        role = RoleManager.update(rolename, version_id, None, f"new description: {index}")
        result = "Success" if role else "Fail"
        return {
            "proccess_index": index,
            "update_result": result
        }

@db_testing_ns.route('/test_optimistic_lock')
class OptimisticLockTest(Resource):
    @db_testing_ns.marshal_list_with(optimistic_lock_result)
    def get(self):
        rolename = "optimistic_lock_test"
        RoleManager.create(rolename, "testing", "testing optimistic lock with 10 processes")
        role = RoleManager.read(rolename)
        
        testing_inputs = [(rolename, index, role.version_id) for index in range(10)]
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.starmap(test_optimistic_lock, testing_inputs)
        return results, 200
