
import os
import subprocess
import time
import json

class RobotTester():
    def __init__(self):
        pass

    def execute_test_cases(self):
        # delete the local test file
        logfile_path = os.path.dirname(os.path.abspath(__file__)) + "/testing_log.json"
        if os.path.exists(logfile_path):
            os.remove(logfile_path)
        
        test_script = os.path.dirname(os.path.abspath(__file__)) + "/test_bridge_py2.py"
        test_command = test_script
        py2_partner = subprocess.call(["gnome-terminal", "--", "python2", test_command])

        while not os.path.exists(logfile_path):
            continue
        
        with open(logfile_path, "r") as logfile:
            results = json.load(logfile)

        user_accepts = None 
        while user_accepts != 'y' and user_accepts != 'n':
            print("TESTS: %d" % len(results['tests']))
            for test in results['tests']:
                print(test)

            print("")
            print("Failures: %d" % len(results['failures']))
            for failure in results['failures']:
                print(failure)

            print("")
            print("Errors: %d" % len(results['errors']))
            for error in results['errors']:
                print(error)

            user_accepts = input("Accept results y/n?: ")


        if user_accepts == 'n':
            raise ValueError('The Robot failed one or more tests. See test/testing_log.json for details.')
            exit()
