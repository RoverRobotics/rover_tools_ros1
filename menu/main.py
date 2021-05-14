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
#from installer.install import RobotPackageInstaller
from mfgdb.records import ManufacturingRecordDb


with open("menu_version.json", "r") as version_file:
    menu_version = json.load(version_file)['MenuVersion']

# determine if this should be the internal or the external version of the tool
if ManufacturingRecordDb.test_credentials(*ManufacturingRecordDb.get_local_credentials()):
    print('valid credentials found!')
    exit()

# Create the menu
menu = ConsoleMenu("Rover Manufacturing Tool v%s" % menu_version, "Tom is a dingus")

# Menu options
f1 = FunctionItem("Install", input, ["Enter an input"])
f2 = FunctionItem("Calibrate", input, ["Enter an input"])
f3 = FunctionItem("Test", input, ["Enter an input"])
f4 = FunctionItem("Full Suite", input, ["Enter an input"])
f5 = FunctionItem("Get Device Information", input, ["Enter an input"])
f6 = FunctionItem("Add Inspection Data", input, ["Enter an input"])
f7 = FunctionItem("Issue Serial Number", input, ["Enter an input"])
f8 = FunctionItem("Retrieve Full PDF", input, ["Enter an input"])
f9 = FunctionItem("Retrieve Install Log", input, ["Enter an input"])


menu.append_item(f1)
menu.append_item(f2)
menu.append_item(f3)
menu.append_item(f4)
menu.append_item(f5)
menu.append_item(f6)
menu.append_item(f7)
menu.append_item(f8)
menu.append_item(f9)

#menu.append_item(command_item)
#menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()