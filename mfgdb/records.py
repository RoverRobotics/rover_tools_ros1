import boto3
import os
import json

ACCESS_ID = "AKIAWVQQ3JAD4QMBRV6A"
ACCESS_KEY = "XUEHHr5QTbsU6gN0IwUJ+8Iw2H1uXbC5ZJZWJ/kW"

class ManufacturingRecordDb():
    def __init__(self, access_id, access_key, db_info_path="config/db_info.json", table_name="ManufacturingRecords", region="us-west-2"):
        
        # register input args
        self.access_id = access_id
        self.access_key = access_key
        self.table_name = table_name
        self.region = region

        # update environment vars
        os.environ['AWS_DEFAULT_REGION'] = self.region

        # create the db resource
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id = self.access_id,
            aws_secret_access_key = self.access_key
        )

        # create the table object
        self.table = self.dynamodb.Table(self.table_name)

        # load a list of mandatory data
        self.db_info_path = db_info_path
        with open(self.db_info_path, "r") as read_file:
            self.db_mandatory_cols = json.load(read_file)['MandatoryColumns']

    def get_robot_information(self, serial_number:str):
        
        response = self.table.get_item(
            Key={
                'SerialNumber': serial_number
            }
        )

        if 'Item' not in response:
            print("Serial Number %s not found in DB!" % serial_number)
            return None
        
        print("ROBOT INFORMATION FOR SERIAL %s" % response['Item']['SerialNumber'])
        for key, value in response['Item'].items():
            if 'SerialNumber' in key:
                continue
            print(key, value)

        return response['Item']

    def register_new_robot(self, item_for_db:dict):
        
        # ensure that all the required columns are present
        for col in self.db_mandatory_cols:
            if col not in item_for_db:
                print('Missing mandatory input for manufacturing DB. DEVICE NOT ADDED TO DB. Please add required information and try again')
                return

        # push item to db
        print("ADDING ROBOT %s to DB" % item_for_db['SerialNumber'])
        self.table.put_item(
            Item=item_for_db
        )

        # validate that the item was pushed successfully
        if self.get_robot_information(item_for_db['SerialNumber']) is not None:
            print('Robot %s successfully added to manufacturing db' % item_for_db['SerialNumber'])
        else:
            print('Failed to add robot to manufacturing DB. Contact Engineering for help')
                

if __name__ == '__main__':
    db = ManufacturingRecordDb(ACCESS_ID, ACCESS_KEY)
    db.get_robot_information("000000")
    db.register_new_robot(
        {
            "SerialNumber":"123456",
            "RobotModel":"Mini",
            "FinalAssemblyNumber":"A700-FOOBAR",
            "FinalAssemblyRevision":"ZZZZZ",
            "FirmwareVersion":"noneofyourbusiness",
            "GUID":"????",
            "Operator":"Obviously TOM",
            "Date":"today",
            "Time":"now",
            "CalibrationData":"calibratedAF",
            "TestResults":"all clear",
            "TestedBy":"dingusboi",
            "InspectionData":"it was all good homie",
            "InspectedBy":"get bent"
        }
    )
    


    

    


