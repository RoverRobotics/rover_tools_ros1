from robottests.movement_unit_tests import get_test_suite, system_ready_for_test
import unittest
import os
import json


def execute_test_cases(test_log_file = os.path.dirname(os.path.abspath(__file__)) + "/testing_log.json"):
 
    operator_name = raw_input("Enter your name: ")
    # collect all the test cases
    if not system_ready_for_test():
        with open(test_log_file, "w") as logfile:
            json.dump(
                {
                    "tests": [],
                    "failures": [],
                    "errors": ["THE SYSTEM WAS NOT TESTED!"],
                    "operator": operator_name
                },
                logfile,
                indent=4,
                sort_keys=True
            )
            return
    
    test_suite = get_test_suite()

    # build a runner
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    result.tests_run = test_suite._tests

    print('test_log_file path ', test_log_file)

    tests = [str(test) for test in result.tests_run]
    failures = [str(failure) for failure in result.failures]
    errors = [str(error) for error in result.errors]

    with open(test_log_file, "w") as logfile:
        json.dump(
            {
                "tests": tests,
                "failures": failures,
                "errors": errors,
                "operator": operator_name
            },
            logfile,
            indent=4,
            sort_keys=True
        )
    

execute_test_cases()



