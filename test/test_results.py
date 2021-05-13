from robottests.movement_unit_tests import get_test_suite
import unittest

def execute_test_cases():
 
    # collect all the test cases
    test_suite = get_test_suite()

    # build a runner
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    print result

    

    #result = runner._makeResult()
    #print result
    
    #result.startTestRun(test_suite)

    #print test_suite
    
    # start the tests
    #result.startTest(RobotTests)

    #print 'Tests successful: ' + str(result.wasSuccessful())
    #print result.testsRun
    #print result.printErrors()


execute_test_cases()

