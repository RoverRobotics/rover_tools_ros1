# Import the necessary packages
import sys
import os
sys.path.append(os.path.join(sys.path[0], "../"))
sys.path.append(os.path.join(sys.path[0], "../", "installer"))
sys.path.append(os.path.join(sys.path[0], "../", "mfgdb"))
sys.path.append(os.path.join(sys.path[0], "../", "test"))
print(sys.path)

from consolemenu import *
from consolemenu.items import *
import json
from install.install import RobotPackageInstaller
from mfgdb.records import ManufacturingRecordDb

with open(os.path.dirname(__file__) + "/menu_version.json", "r") as version_file:
    menu_version = json.load(version_file)['MenuVersion']

# determine if this should be the internal or the external version of the tool
launch_production_menu = ManufacturingRecordDb.test_credentials(*ManufacturingRecordDb.get_local_credentials())

# get a list of all the models
robots = RobotPackageInstaller.get_models()

# Create the menu
if launch_production_menu:
    menu = ConsoleMenu("Rover Manufacturing Tool v%s" % menu_version, "Internal Tools")
else:
    menu = ConsoleMenu("Rover Manufacturing Tool v%s" % menu_version, "Customer Tools")

# install_functions
installer = RobotPackageInstaller()
install_submenu = ConsoleMenu("Select Model")
install_functions = [FunctionItem(robot, installer.run_install, kwargs={"model":robot}) for robot in robots]
for func in install_functions:
    install_submenu.append_item(func)

install_submenu_item = SubmenuItem("Install", install_submenu, menu)




# f1 = SubmenuItem("Install", SelectionMenu(robots)., menu)
#f2 = SubmenuItem("Calibrate", SelectionMenu(robots), menu)
#f3 = SubmenuItem("Test", SelectionMenu(robots), menu)
#f4 = SubmenuItem("Full Suite", SelectionMenu(robots), menu)
#f5 = SubmenuItem("Get Device Information", SelectionMenu(robots), menu)
#f6 = SubmenuItem("Add Inspection Data", SelectionMenu(robots), menu)
# f7 = SubmenuItem("Issue Serial Number", SelectionMenu(robots), menu)
# f8 = SubmenuItem("Retrieve Full PDF", SelectionMenu(robots), menu)
# f9 = SubmenuItem("Retrieve Install Log", SelectionMenu(robots), menu)

menu.append_item(install_submenu_item)
#menu.append_item(f1)
#menu.append_item(f2)
#menu.append_item(f3)
#menu.append_item(f4)
#menu.append_item(f5)
#menu.append_item(f6)
# menu.append_item(f7)
# menu.append_item(f8)
# menu.append_item(f9)

#menu.append_item(command_item)
#menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()