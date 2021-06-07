# Import the necessary packages
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

print(sys.path)
from consolemenu import *
from consolemenu.items import *
import json
from install.install import RobotPackageInstaller
from mfgdb.records import ManufacturingRecordDb, DeviceInformation
from testing.test_bridge import RobotTester
from mfg_setup import mfg_setup
from calibration.calibration import RobotCalibrator
from shared.utils import user_says_yes
from inspection.inspection import ManualInspection
from menu.menu_install import build_install_submenu
from menu.menu_serial_number import build_serial_number_function
from menu.menu_inspection import build_inspection_submenu
from menu.menu_calibration import build_calibration_submenu

with open(os.path.dirname(__file__) + "/tool_version.json", "r") as version_file:
    tool_version = json.load(version_file)['ToolVersion']

# determine if this should be the internal or the external version of the tool
launch_production_menu = ManufacturingRecordDb.test_credentials(*ManufacturingRecordDb.get_local_credentials())
mfgdb = None if not launch_production_menu else ManufacturingRecordDb(*ManufacturingRecordDb.get_local_credentials())

# Create the menu
if launch_production_menu:
    menu = ConsoleMenu("Rover Manufacturing Tool v%s" % tool_version, "Internal Tools")
else:
    menu = ConsoleMenu("Rover Manufacturing Tool v%s" % tool_version, "Customer Tools")

# start with no serial number
device_serial_number = None

# calibration


# tester
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

test_submenu_item = SubmenuItem("Test", test_submenu, menu)

# register device data
device_info = DeviceInformation()

def device_info_main():
    try:
        device_info.query_user()
        if device_info.user_confirms_data_():
            if not mfgdb.register_robot(device_info.get_entered_data()):
                raise ValueError('did not publish device data to cloud')
    except Exception as e:
        print('Problem during data entry')
        print(e)
        input('press any key to continue')

device_info_function = FunctionItem("Register Device", device_info_main)

# build GUI
if mfgdb is not None:
    menu.append_item(build_serial_number_function(mfgdb))
if mfgdb is not None:
    menu.append_item(build_inspection_submenu(menu, mfgdb))
menu.append_item(build_install_submenu(menu, mfgdb))
menu.append_item(build_calibration_submenu(menu, mfgdb))
menu.append_item(test_submenu_item)
if mfgdb is not None:
    menu.append_item(device_info_function)

# Finally, we call show to show the menu and allow the user to interact
menu.show()