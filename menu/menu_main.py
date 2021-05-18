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
from mfgdb.records import ManufacturingRecordDb
from testing.test_bridge import RobotTester


with open(os.path.dirname(__file__) + "/menu_version.json", "r") as version_file:
    menu_version = json.load(version_file)['MenuVersion']

# determine if this should be the internal or the external version of the tool
launch_production_menu = ManufacturingRecordDb.test_credentials(*ManufacturingRecordDb.get_local_credentials())
mfgdb = None if not launch_production_menu else ManufacturingRecordDb(*ManufacturingRecordDb.get_local_credentials())

# Create the menu
if launch_production_menu:
    menu = ConsoleMenu("Rover Manufacturing Tool v%s" % menu_version, "Internal Tools")
else:
    menu = ConsoleMenu("Rover Manufacturing Tool v%s" % menu_version, "Customer Tools")

# start with no serial number
device_serial_number = None

# installer
robots = RobotPackageInstaller.get_models()
installer = RobotPackageInstaller()
install_submenu = ConsoleMenu("Select Model")

def installer_main(model:str):
    device_serial_number = input("Enter serial number: ")
    installer.run_install(model=model)
    if mfgdb is not None:
        if not mfgdb.publish_install_log(os.path.dirname(__file__) + "/../install/install.log", device_serial_number):
            raise ValueError('Failed to publish install log to cloud. Halting.')


install_functions = [FunctionItem(robot, installer_main, kwargs={"model":robot}) for robot in robots]
for func in install_functions:
    install_submenu.append_item(func)

install_submenu_item = SubmenuItem("Install", install_submenu, menu)

# tester
tester = RobotTester()

def tester_main():
    device_serial_number = input("Enter serial number: ")
    tester.execute_test_cases()
    if mfgdb is not None:
        if not mfgdb.publish_test_log(os.path.dirname(__file__) + "/../testing/testing_log.json", device_serial_number):
            raise ValueError('Failed to publish test log to cloud. Halting.')

test_function = FunctionItem("Test", tester_main)

menu.append_item(install_submenu_item)
menu.append_item(test_function)

# Finally, we call show to show the menu and allow the user to interact
menu.show()