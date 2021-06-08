from consolemenu import *
from consolemenu.items import *
from mfgdb.records import ManufacturingRecordDb
from shared.utils import user_says_yes

def build_serial_number_function(mfgdb:ManufacturingRecordDb):
    def issue_serial_number():
        try:
            nas = mfgdb.get_next_available_serial()
            print('')
            print('The next available serial number is: %s' % str(nas))
            if user_says_yes("Issue serial number now?"):
                success = mfgdb.register_sn(nas)
                if not success:
                    raise ValueError('Failed to register sn with db...')
            input('press any key to continue')
        except Exception as e:
            print('Problem while finding next available serial number from mfg db...')
            print(e)
            input('press any key to continue')

    return FunctionItem("Issue Serial Number", issue_serial_number)


