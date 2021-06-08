from consolemenu import *
from consolemenu.items import *
from mfgdb.records import ManufacturingRecordDb
from shared.utils import user_says_yes
import pexpect

def build_records_submenu(menu, mfgdb:ManufacturingRecordDb):
    
    records_submenu = ConsoleMenu("Records: Select Action")
    
    def check_records():
        try:
            serialnum = str(input("Enter serial number: "))
            _ = mfgdb.check_db_entries(serialnum)
            input('press any key to continue')
        except Exception as e:
            print('Records FAILURE')
            print(e)
            input('press any key to continue.')

    def view_records():
        try:
            serialnum = str(input("Enter serial number: "))
            files = mfgdb.download_db_entries(serialnum=serialnum)

            for filename, path in files.items():
                if user_says_yes("View %s" % filename):
                    in_terminal_program = pexpect.spawn("nano " + path)
                    in_terminal_program.interact()
            input('press any key to continue')
        except Exception as e:
            print('Records FAILURE')
            print(e)
            input('press any key to continue.')

    
    records_functions = [
        FunctionItem('Check DB records for SN', check_records),
        FunctionItem('View Records', view_records)]
    
    for func in records_functions:
        records_submenu.append_item(func)

    return SubmenuItem("Records", records_submenu, menu)