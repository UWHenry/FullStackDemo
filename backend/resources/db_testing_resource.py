import multiprocessing
import os
from typing import Tuple

from flask_restx import Resource
from flask import Flask
from flask_jwt_extended import jwt_required
from sqlalchemy.orm.exc import StaleDataError

from db_utils.role_manager import RoleManager
from .namespace_models import api_ns, test_result
from models import db


def test_optimistic_lock(rolename: str, index: int) -> Tuple[int, str]:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    db.init_app(app)
    with app.app_context():
        result = None
        try:
            with db.session.begin_nested():
                role = RoleManager.read(rolename)
                if role:
                    RoleManager.update(role, None, f"new description {index}", None)
                    db.session.commit()
                    result = "Success"
                else:
                    result = "Role Not Found"
        except StaleDataError:
            db.session.rollback()
            result = "Optimistic Lock Conflict"
        return {
            "process_id": index,
            "update_result": result
        }

@api_ns.route('/test_optimistic_lock')
class OptimisticLockTest(Resource):
    @api_ns.marshal_list_with(test_result)
    @jwt_required()
    def get(self):
        ROLENAME = "optimistic_lock_test"
        # create role if not Exist
        try:
            with db.session.begin_nested():
                RoleManager.create(ROLENAME, "testing", "testing optimistic lock with 10 processes", [])
                db.session.commit()
        except:
            db.session.rollback()
        # creates 10 processes trying to update the database
        testing_inputs = [(ROLENAME, index) for index in range(10)]
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.starmap(test_optimistic_lock, testing_inputs)
        return results, 200