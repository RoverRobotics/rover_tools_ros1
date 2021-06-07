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

# serial number utility

def issue_serial_number():
    try:
        nas = mfgdb.get_next_available_serial()
        print('The next available serial number is: %s' % str(nas))
        input('press any key to continue')
    except Exception as e:
        print('Problem while finding next available serial number from mfg db...')
        print(e)
        input('press any key to continue')

serial_number_function = FunctionItem("Issue Serial Number", issue_serial_number)

# installer
robots = RobotPackageInstaller.get_models()
installer = RobotPackageInstaller()
install_submenu = ConsoleMenu("Installation: Select Model")

def installer_main(model:str):
    try:
        print('Starting install, please wait.')
        installer.run_install(model=model, verification_file_header="tool version: " + tool_version)
        installer.print_verification_results()
        input('Installation complete. Press enter to continue.')
        if mfgdb is not None:
            if not user_says_yes("Publish results to cloud?"):
                return
            device_serial_number = input("Enter serial number: ")
            if not mfgdb.publish_install_log(os.path.dirname(__file__) + "/../install/install.log", device_serial_number):
                raise ValueError('Failed to publish install log to cloud. Halting.')

            verification_file = installer.get_verification_file()
            if verification_file is not None:
                if not mfgdb.publish_install_log(verification_file, "verify_" + device_serial_number):
                    raise ValueError('Failed to publish verification log to cloud. Halting.')
    except Exception as e:
        print('Install FAILURE')
        print(e)
        input('press any key to continue.')


install_functions = [FunctionItem(robot, installer_main, kwargs={"model":robot}) for robot in robots]
for func in install_functions:
    install_submenu.append_item(func)

install_submenu_item = SubmenuItem("Install", install_submenu, menu)

# inspection
inspection_mgr = ManualInspection()
robots = inspection_mgr.get_models()
inspect_submenu = ConsoleMenu("Inspection: Select Model")

def inspection_main(model:str):
    try:
        print('Starting manual inspection procedure, please wait.')
        results = inspection_mgr.run_inspection(model)

        print('')
        print('INSPECTION RESULTS: ')
        print('')
        for name, result in results.items():
            print("%s: %s" % (name, result))

        print('')
        input('inspection complete, press any key to continue')
        
        if mfgdb is not None:
            print('do stuff')

    except Exception as e:
        print('Inspection FAILURE')
        print(e)
        input('press any key to continue.')

inspect_functions = [FunctionItem(robot, inspection_main, kwargs={"model":robot}) for robot in robots]
for func in inspect_functions:
    inspect_submenu.append_item(func)

inspect_submenu_item = SubmenuItem("Inspection", inspect_submenu, menu)

# calibration
calibrator = RobotCalibrator()
calibration_submenu = ConsoleMenu("Calibration: Select Model")
robots = mfg_setup.get_models()
def calibration_main(model:str):
    try:
        print('Starting calibration, please wait.')
        calibrator.run_calibration(model=model)
        # installer.print_verification_results()
        input('Calibration complete. Press enter to continue.')
        if mfgdb is not None:
            if not user_says_yes("Publish results to cloud?"):
                return
            device_serial_number = input("Enter serial number: ")
            if not mfgdb.publish_install_log(os.path.dirname(__file__) + "/../install/install.log", device_serial_number):
                raise ValueError('Failed to publish install log to cloud. Halting.')

            verification_file = installer.get_verification_file()
            if verification_file is not None:
                if not mfgdb.publish_install_log(verification_file, "verify_" + device_serial_number):
                    raise ValueError('Failed to publish verification log to cloud. Halting.')
    except Exception as e:
        print('Calibration FAILURE')
        print(e)
        input('press any key to continue.')

    #if mfgdb is not None:
    #    input("calibration is not supported in this version. Press Enter to continue.")

calibration_functions = [FunctionItem(robot, calibration_main, kwargs={"model":robot}) for robot in robots]
for func in calibration_functions:
    calibration_submenu.append_item(func)

calibration_submenu_item = SubmenuItem("Calibrate", calibration_submenu, menu)

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
    menu.append_item(serial_number_function)
if mfgdb is not None:
    menu.append_item(inspect_submenu_item)
menu.append_item(install_submenu_item)
menu.append_item(calibration_submenu_item)
menu.append_item(test_submenu_item)
if mfgdb is not None:
    menu.append_item(device_info_function)

# Finally, we call show to show the menu and allow the user to interact
menu.show()