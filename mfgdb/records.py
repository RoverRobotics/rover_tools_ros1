import boto3
import os
import json
from shared.utils import user_says_yes

class ManufacturingRecordDb():
    def __init__(
        self, 
        access_id, 
        access_key, 
        db_info_path=(os.path.dirname(__file__) + "/db_info.json"), 
        table_name="ManufacturingRecords", 
        region="us-west-2"
    ):
        
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

        # create the filestore resource (for logs)
        self.s3 = boto3.client(
            's3',
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

    def register_robot(self, item_for_db:dict):
        
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
        confirmation = self.get_robot_information(item_for_db['SerialNumber'])
        if confirmation is not None:
            print('Robot %s successfully added to manufacturing db' % item_for_db['SerialNumber'])
        else:
            print('Failed to add robot to manufacturing DB. Contact Engineering for help')

        return confirmation

    def publish_install_log(self, logfile_path:str, filename:str):
        try:
            response = self.s3.upload_file(logfile_path, "rr-install-logs", filename + ".log")
            print(response)
        except Exception as e:
            print('Failed to publish log %s' % e)
            return False

        return True

    def publish_test_log(self, logfile_path:str, serial_number:str):
        try:
            response = self.s3.upload_file(logfile_path, "rr-mfg-test-logs", "log_" + serial_number + ".json")
            print(response)
        except Exception as e:
            print('Failed to publish log %s' % e)
            return False

        return True
    

    def get_local_credentials(credential_file=("/media/rover/install_stick/credentials.json")):
        try:
            with open(credential_file, "r") as read_file:
                credentials = json.load(read_file)

            return credentials["ACCESS_ID"], credentials["ACCESS_KEY"]
        except:
            print('Unable to find local credentials')
            return None, None

    def test_credentials(access_id, access_key):
        os.environ['AWS_DEFAULT_REGION'] = "us-west-2"
        sts = boto3.client(
            'sts',
            aws_access_key_id = access_id,
            aws_secret_access_key = access_key
        )
        try:
            sts.get_caller_identity()
        except:
            return False

        return True


class DeviceInformation():
    def __init__(self, required_fields_file =(os.path.dirname(__file__) + "/db_info.json")):

        self.device_data = {}
        with open(required_fields_file, "r") as f:
            self.required_fields = json.load(f)

        self.device_data = {k:None for k in self.required_fields}

    def query_user(self):
        print('Please enter the following data...')
        for field in self.required_fields:
            self.device_data[field] = input("%s: ")
            
    def user_confirms_data(self):
        print('Please confirm the data below...')

        for k, v in self.device_data.items():
            print("%s: %s" % (k, v))

        if not user_says_yes("Data correct?"):
            print('please run data entry again...')
            input('press any key to continue')
            return False
        else:
            return True

if __name__ == '__main__':
    pass
    


    

    


