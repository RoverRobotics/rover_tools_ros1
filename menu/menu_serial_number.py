from consolemenu import *
from consolemenu.items import *

def build_serial_number_function(mfgdb):
    def issue_serial_number():
        try:
            nas = mfgdb.get_next_available_serial()
            print('The next available serial number is: %s' % str(nas))
            input('press any key to continue')
        except Exception as e:
            print('Problem while finding next available serial number from mfg db...')
            print(e)
            input('press any key to continue')

    return FunctionItem("Issue Serial Number", issue_serial_number)


