from flask_restx  import Namespace, Resource
import multiprocessing
from models.role import Role
from db_utils.role_manager import RoleManager
import time
import random
from flask import Flask
from models import db
def test_update(index):
    # Create a new Flask application for each process
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://my_user:my_password@localhost:5432/my_db"
    

    # Initialize the database with the app
    db.init_app(app)
    with app.app_context():
        testing_rolename = "optimistic_lock_test"
        role = Role.query.get(testing_rolename)
        role.description = f"new description {index}"
        role.version_id += 1
        time.sleep((10 - index) * 1)
        try:
            commit_time = time.time()
            db.session.commit()
            result = "Success"
        except:
            db.session.rollback()
            result = "Fail"
        # result = RoleManager.update(testing_rolename, None, f"new description {index}")
        return (index, result, commit_time)


db_testing_ns = Namespace("db_testing")
testing_rolename = "optimistic_lock_test"
# def test_update(index):
#     result = RoleManager.update(testing_rolename, None, "new description")
#     return (index, result)

@db_testing_ns.route('/test_optimistic_lock')
class OptimisticLockTest(Resource):
    def get(self):
        # initialize testing role
        RoleManager.create(testing_rolename, "testing", "testing optimistic lock with 10 processes")
        
        update_data = [i for i in range(10)]
        # launch processes
        with multiprocessing.Pool(processes=10) as pool:
            results = pool.map(test_update, update_data)
        
        return results, 200