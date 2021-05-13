
from mfgdb.records import ManufacturingRecordDb
from test.test import RobotTester


if __name__ == '__main__':
    
    access_id, access_key = ManufacturingRecordDb.get_local_credentials()
    if access_id is not None and access_key is not None:
        db = ManufacturingRecordDb(access_id, access_key)
    else:
        db = None

    if db is not None:
        db.get_robot_information("123456")
