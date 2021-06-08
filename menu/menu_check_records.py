from consolemenu import *
from consolemenu.items import *
from mfgdb.records import ManufacturingRecordDb
from shared.utils import user_says_yes

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

    
    records_functions = [FunctionItem('Check DB records for SN', check_records)]
    for func in records_functions:
        records_submenu.append_item(func)

    return SubmenuItem("Records", records_submenu, menu)