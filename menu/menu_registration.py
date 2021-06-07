from consolemenu import *
from consolemenu.items import *
from mfgdb.records import DeviceInformation
from shared.utils import user_says_yes

def build_device_registration_function(mfgdb):
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

    return FunctionItem("Register Device", device_info_main)