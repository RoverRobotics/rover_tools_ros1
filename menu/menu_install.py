from install.install import RobotPackageInstaller
from consolemenu import *
from consolemenu.items import *
from shared.utils import user_says_yes
import os
import json

def build_install_submenu(menu, mfgdb=None, tool_version_file = os.path.dirname(__file__) + "/tool_version.json"):
    # installer
    robots = RobotPackageInstaller.get_models()
    installer = RobotPackageInstaller()
    install_submenu = ConsoleMenu("Installation: Select Model")
    with open(tool_version_file, "r") as f:
        tool_version = json.load(f)["ToolVersion"]

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

    return SubmenuItem("Install", install_submenu, menu)
