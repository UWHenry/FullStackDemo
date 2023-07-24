from flask_restx  import Namespace, Resource
import multiprocessing
from db_utils.role_manager import RoleManager

db_testing_ns = Namespace("db_testing")
testing_rolename = "optimistic_lock_test"
def test(index, result_destination):
    result = RoleManager.update(testing_rolename, None, "new description")
    result_destination.put((index, result))

@db_testing_ns.route('/test_optimistic_lock')
class OptimisticLockTest(Resource):
    def get(self):
        # initialize testing role
        RoleManager.create(testing_rolename, "testing", "testing optimistic lock with 10 processes")
        
        # set up result queue and testing functions
        result_queue = multiprocessing.Queue()
        
        # launch processes
        processes = []
        for i in range(10):
            process = multiprocessing.Process(target=test, args=(i, result_queue))
            process.start()
            processes.append(process)
        # wait for process to finish
        for process in processes:
            process.join()
        
        # gather results
        results = {}
        while not result_queue.empty():
            index, result = result_queue.get()
            print(result)
            results[index] = result
        
        return results, 200