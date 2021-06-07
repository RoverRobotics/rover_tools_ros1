from consolemenu import *
from consolemenu.items import *
from calibration.calibration import RobotCalibrator
from shared.utils import user_says_yes
from mfg_setup import mfg_setup

def build_calibration_submenu(menu, mfgdb=None):
    calibrator = RobotCalibrator()
    calibration_submenu = ConsoleMenu("Calibration: Select Model")
    robots = mfg_setup.get_models()
    def calibration_main(model:str):
        try:
            print('Starting calibration, please wait.')
            calibrator.run_calibration(model=model)
            # installer.print_verification_results()
            input('Calibration complete. Press enter to continue.')
            if mfgdb is not None:
                if not user_says_yes("Publish results to cloud?"):
                    return
                print('do stuff here in the future')
        except Exception as e:
            print('Calibration FAILURE')
            print(e)
            input('press any key to continue.')

    calibration_functions = [FunctionItem(robot, calibration_main, kwargs={"model":robot}) for robot in robots]
    for func in calibration_functions:
        calibration_submenu.append_item(func)

    return SubmenuItem("Calibrate", calibration_submenu, menu)