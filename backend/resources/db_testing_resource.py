import multiprocessing
import os
import time
from typing import Tuple

from flask_restx import Resource
from flask import Flask
from flask_jwt_extended import jwt_required

from db_utils.role_manager import RoleManager
from db_utils.user_manager import UserManager
from .namespace_models import db_testing_ns, test_result
from models import db


def test_optimistic_lock(rolename: str, index: int, version_id: int, sleep_time: int) -> Tuple[int, str]:
    """
    Initializes a new flask app, setup database connections, and update the database.
    version_id is retrived prior to process creation to simulate resource competition.
    One the first process should update successfully since it updates first, sleeping time in implemented to increase the time gap.
    """
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://my_user:my_password@localhost:5432/my_db"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    db.init_app(app)
    with app.app_context():
        time.sleep(sleep_time)
        role = RoleManager.update(rolename, version_id, None, f"new description: {index}", None)
        result = "Success" if role else "Fail"
        return {
            "proccess_index": index,
            "update_result": result
        }

@db_testing_ns.route('/test_optimistic_lock')
class OptimisticLockTest(Resource):
    @db_testing_ns.marshal_list_with(test_result)
    @jwt_required()
    def get(self):
        rolename = "optimistic_lock_test"
        RoleManager.create(rolename, "testing", "testing optimistic lock with 10 processes", [])
        role = RoleManager.read(rolename)
        
        testing_inputs = [(rolename, index, role.version_id, 0 if index == 0 else 1) for index in range(10)]
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.starmap(test_optimistic_lock, testing_inputs)
        return results, 200


# def test_transaction(rolename: str, index: int, version_id: int) -> Tuple[int, str]:
#     """
#     Initializes a new flask app, setup database connections, and update the database.
#     version_id is retrived prior to process creation to simulate resource competition.
    
#     """
#     app = Flask(__name__)
#     app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://my_user:my_password@localhost:5432/my_db"
#     # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#     db.init_app(app)
#     with app.app_context():
#         role = RoleManager.update(rolename, version_id, None, f"new description: {index}")
#         result = "Success" if role else "Fail"
#         return {
#             "proccess_index": index,
#             "update_result": result
#         }

# @db_testing_ns.route('/test_transaction')
# class TransactionTest(Resource):
#     @db_testing_ns.marshal_list_with(test_result)
#     def get(self):
#         rolename = "transaction_test"
#         RoleManager.create(rolename, "testing", "testing optimistic lock with 10 processes")
#         role = RoleManager.read(rolename)
        
#         testing_inputs = [(rolename, index, role.version_id) for index in range(10)]
#         with multiprocessing.Pool(processes=10) as pool:
#             results = pool.starmap(test_optimistic_lock, testing_inputs)
#         return results, 200