
class RobotTester():
    def __init__():
        pass

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