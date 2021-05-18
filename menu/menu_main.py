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
from calibration.calibration import RobotCalibrator

def user_says_yes(question:str):
    user_input = None
    while user_input != 'y' and user_input != 'n':
        user_input = input(question + " (y/n):")

    if user_input == 'y':
        return True
    else:
        return False


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
install_submenu = ConsoleMenu("Installation: Select Model")

def installer_main(model:str):
    print('Starting install, please wait.')
    installer.run_install(model=model)
    installer.print_verification_results()
    input('Installation complete. Press enter to continue.')
    if mfgdb is not None:
        if not user_says_yes("Publish results to cloud?"):
            return
        device_serial_number = input("Enter serial number: ")
        if not mfgdb.publish_install_log(os.path.dirname(__file__) + "/../install/install.log", device_serial_number):
            raise ValueError('Failed to publish install log to cloud. Halting.')


install_functions = [FunctionItem(robot, installer_main, kwargs={"model":robot}) for robot in robots]
for func in install_functions:
    install_submenu.append_item(func)

install_submenu_item = SubmenuItem("Install", install_submenu, menu)

# calibration
calibrator = RobotCalibrator()
calibration_submenu = ConsoleMenu("Calibration: Select Model")

def calibration_main(model:str):
    input("calibration is not supported in this version. Press Enter to continue.")
    calibrator.calibrate(model=model)
    #if mfgdb is not None:
    #    input("calibration is not supported in this version. Press Enter to continue.")

calibration_functions = [FunctionItem(robot, calibration_main, kwargs={"model":robot}) for robot in robots]
for func in calibration_functions:
    calibration_submenu.append_item(func)

calibration_submenu_item = SubmenuItem("Calibrate", calibration_submenu, menu)

# tester
tester = RobotTester()
test_submenu = ConsoleMenu("Testing: Select Model")

def tester_main(model:str):
    acceptance = tester.execute_test_cases()
    if acceptance:
        if mfgdb is not None:
            if user_says_yes("Publish results to cloud?"):
                device_serial_number = input("Enter serial number: ")
                if not mfgdb.publish_test_log(os.path.dirname(__file__) + "/../testing/testing_log.json", device_serial_number):
                    input('Failed to publish results to cloud. Contact your system administrator.')
            else:
                input("Did not publish results to cloud. Push Enter to continue.")

test_functions = [FunctionItem(robot, tester_main, kwargs={'model':robot}) for robot in robots]
for func in test_functions:
    test_submenu.append_item(func)

test_submenu_item = SubmenuItem("Test", test_submenu, menu)

# register 

menu.append_item(install_submenu_item)
menu.append_item(calibration_submenu_item)
menu.append_item(test_submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()