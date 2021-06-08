# Import the necessary packages
import sys
import os
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", ".."))
sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), ".."))

print(sys.path)
from consolemenu import *
from consolemenu.items import *
import json
from mfgdb.records import ManufacturingRecordDb
from menu.menu_install import build_install_submenu
from menu.menu_serial_number import build_serial_number_function
from menu.menu_inspection import build_inspection_submenu
from menu.menu_calibration import build_calibration_submenu
from menu.menu_testing import build_testing_submenu
from menu.menu_registration import build_device_registration_function
from menu.menu_check_records import build_records_submenu

with open(os.path.dirname(__file__) + "/tool_version.json", "r") as version_file:
    tool_version = json.load(version_file)['ToolVersion']

# determine if this should be the internal or the external version of the tool
launch_production_menu = ManufacturingRecordDb.test_credentials(*ManufacturingRecordDb.get_local_credentials())
mfgdb = None if not launch_production_menu else ManufacturingRecordDb(*ManufacturingRecordDb.get_local_credentials())

# Create the menu
if launch_production_menu:
    menu = ConsoleMenu("Rover Tools v%s" % tool_version, "Internal Use")
else:
    menu = ConsoleMenu("Rover Tools v%s" % tool_version, "Customer Tools")

# build GUI below ..............

# serial number
if launch_production_menu:
    menu.append_item(build_serial_number_function(mfgdb))

# inspection
if launch_production_menu:
    menu.append_item(build_inspection_submenu(menu, mfgdb))

# installation
menu.append_item(build_install_submenu(menu, mfgdb))

# calibration
menu.append_item(build_calibration_submenu(menu, mfgdb))

# testing
menu.append_item(build_testing_submenu(menu, mfgdb))

# device registration
if launch_production_menu:
    menu.append_item(build_device_registration_function(mfgdb))

if launch_production_menu:
    menu.append_item(build_records_submenu(menu, mfgdb))

# Finally, we call show to show the menu and allow the user to interact
menu.show()