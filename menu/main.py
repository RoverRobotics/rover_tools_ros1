# Import the necessary packages
from consolemenu import *
from consolemenu.items import *
import json

with open("menu_version.json", "r") as version_file:
    menu_version = json.load(version_file)['MenuVersion']

# Create the menu
menu = ConsoleMenu("Rover Manufacturing Tool v%s" % menu_version, "Tom is a dingus")

# Menu options
f1 = FunctionItem("Install Only", input, ["Enter an input"])
f2 = FunctionItem("Calibrate Only", input, ["Enter an input"])
f3 = FunctionItem("Test Only", input, ["Enter an input"])
f4 = FunctionItem("Full Suite", input, ["Enter an input"])
f5 = FunctionItem("Get Device Information", input, ["Enter an input"])
f6 = FunctionItem("Add Inspection Data", input, ["Enter an input"])

# Create some items
# MenuItem is the base class for all items, it doesn't do anything when selected
#menu_item = MenuItem("Menu Item")

# A FunctionItem runs a Python function when selected
function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# A CommandItem runs a console command
command_item = CommandItem("Run a console command",  "touch hello.txt")

# A SelectionMenu constructs a menu from a list of strings
selection_menu = SelectionMenu(["item1", "item2", "item3"])

# A SubmenuItem lets you add a menu (the selection_menu above, for example)
# as a submenu of another menu
submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# Once we're done creating them, we just add the items to the menu
#menu.append_item(menu_item)
menu.append_item(f1)
menu.append_item(f2)
menu.append_item(f3)
menu.append_item(f4)
menu.append_item(f5)
menu.append_item(f6)

menu.append_item(command_item)
menu.append_item(submenu_item)

# Finally, we call show to show the menu and allow the user to interact
menu.show()