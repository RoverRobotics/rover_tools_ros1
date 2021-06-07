from consolemenu import *
from consolemenu.items import *
from inspection.inspection import ManualInspection
from shared.utils import user_says_yes

def build_inspection_submenu(menu, mfgdb=None):
    inspection_mgr = ManualInspection()
    robots = inspection_mgr.get_models()
    inspect_submenu = ConsoleMenu("Inspection: Select Model")

    def inspection_main(model:str):
        try:
            print('Starting manual inspection procedure, please wait.')
            results = inspection_mgr.run_inspection(model)

            print('')
            print('INSPECTION RESULTS: ')
            print('')
            for name, result in results.items():
                print("%s: %s" % (name, result))

            print('')
            input('inspection complete, press any key to continue')
            
            if mfgdb is not None:
                if not user_says_yes("Publish results to cloud?"):
                    return

        except Exception as e:
            print('Inspection FAILURE')
            print(e)
            input('press any key to continue.')

    inspect_functions = [FunctionItem(robot, inspection_main, kwargs={"model":robot}) for robot in robots]
    for func in inspect_functions:
        inspect_submenu.append_item(func)

    return SubmenuItem("Inspection", inspect_submenu, menu)