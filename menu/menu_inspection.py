from mfgdb.records import ManufacturingRecordDb
from consolemenu import *
from consolemenu.items import *
from inspection.inspection import ManualInspection
from shared.utils import user_says_yes

def build_inspection_submenu(menu, mfgdb:ManufacturingRecordDb=None):
    inspection_mgr = ManualInspection()
    robots = inspection_mgr.get_models()
    inspect_submenu = ConsoleMenu("Inspection: Select Model")

    def inspection_main(model:str):
        try:
            print('Starting manual inspection procedure, please wait.')
            inspection_passed = inspection_mgr.run_inspection(model)

            inspection_mgr.print_summary()
            print('')
            input('inspection complete, press any key to continue')
            
            if mfgdb is not None:
                if user_says_yes("Publish results to cloud?"):
                    if not inspection_passed:
                        if not user_says_yes("There were one or more failures. Are you sure you want to publish these results?"):
                            return

                    serial = str(input('Enter serial number: '))
                    if not mfgdb.publish_inspection_log(inspection_mgr.get_results_file(), serial):
                        raise ValueError('Failed to publish verification log to cloud. Halting.')
                return

        except Exception as e:
            print('Inspection FAILURE')
            print(e)
            input('press any key to continue.')

    inspect_functions = [FunctionItem(robot, inspection_main, kwargs={"model":robot}) for robot in robots]
    for func in inspect_functions:
        inspect_submenu.append_item(func)

    return SubmenuItem("Inspection", inspect_submenu, menu)