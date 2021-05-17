from robottests.movement_unit_tests import get_test_suite
import unittest
from multiprocessing.connection import Listener

def execute_test_cases():
 
    # collect all the test cases
    test_suite = get_test_suite()

    # build a runner
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)
    print result

    # should ideally return a tuple (boolean, results )
    return result
    

address = ('localhost', 6000)
listener = Listener(address, authkey='arbitrary')
conn = listener.accept()

while True:
    msg = conn.recv()
    if msg = 'execute':
        results = execute_test_cases()
        conn.send(results)
    else:
        conn.close()


