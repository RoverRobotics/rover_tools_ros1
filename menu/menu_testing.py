from consolemenu import *
from consolemenu.items import *
from testing.test_bridge import RobotTester
from shared.utils import user_says_yes
from mfg_setup import mfg_setup
import os

def build_testing_submenu(menu, mfgdb=None):
    tester = RobotTester()
    test_submenu = ConsoleMenu("Testing: Select Model")
    robots = mfg_setup.get_models()
    def tester_main(model:str):
        try:
            acceptance = tester.execute_test_cases(model)
            if acceptance:
                if mfgdb is not None:
                    if user_says_yes("Publish results to cloud?"):
                        device_serial_number = input("Enter serial number: ")
                        if not mfgdb.publish_test_log(os.path.dirname(__file__) + "/../testing/testing_log.json", device_serial_number):
                            input('Failed to publish results to cloud. Contact your system administrator.')
                        if not mfgdb.publish_test_log(
                            os.path.dirname(__file__) + "/../testing/robottests/unittest.log", "utestdebug_" + device_serial_number,
                            format=".log"
                        ):
                            input('Failed to publish results to cloud. Contact your system administrator.')
                    else:
                        input("Did not publish results to cloud. Push Enter to continue.")
            else:
                input("One or more problems were encountered during testing. See above. Press Enter to return to menu.")
        except Exception as e:
            print('Problem executing testing')
            print(e)
            input('press any key to continue')

    test_functions = [FunctionItem(robot, tester_main, kwargs={'model':robot}) for robot in robots]
    for func in test_functions:
        test_submenu.append_item(func)

    return SubmenuItem("Test", test_submenu, menu)