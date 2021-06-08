
import os
import subprocess
import time
import json
import pexpect
from mfg_setup import mfg_setup

class RobotTester():
    def __init__(self):
        pass

    def execute_test_cases(self, model, logfile_path=os.path.dirname(os.path.abspath(__file__)) + "/testing_log.json"):
        # delete the local test file
        if os.path.exists(logfile_path):
            os.remove(logfile_path)

        # put the robot in the correct mode
        mfg_setup.launch_robot_mode(model, mode="mfg_mode")
        
        test_script = os.path.dirname(os.path.abspath(__file__)) + "/test_bridge_py2.py"
        test_command = test_script
        #py2_partner = subprocess.call(["gnome-terminal", "--", "python2", test_command])
        py2_partner = pexpect.spawn("python2 " + test_command)
        py2_partner.interact()
        while not os.path.exists(logfile_path):
            continue
        
        with open(logfile_path, "r") as logfile:
            results = json.load(logfile)

        
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

        # put the robot in the correct mode
        mfg_setup.launch_robot_mode(model, mode="normal_mode")

        input('press any key to continue')

        if len(results['failures']) == 0 and len(results['errors']) == 0:
            return True
        else:
            return False
