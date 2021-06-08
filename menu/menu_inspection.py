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
            inspection_passed = inspection_mgr.run_inspection(model)

            inspection_mgr.print_summary()
            print('')
            input('inspection complete, press any key to continue')
            
            if mfgdb is not None:
                if user_says_yes("Publish results to cloud?"):
                    if not inspection_passed:
                        if user_says_yes("There were one or more failures. Are you sure you want to publish these results?"):
                            print('do something')

                return
                    

        except Exception as e:
            print('Inspection FAILURE')
            print(e)
            input('press any key to continue.')

    inspect_functions = [FunctionItem(robot, inspection_main, kwargs={"model":robot}) for robot in robots]
    for func in inspect_functions:
        inspect_submenu.append_item(func)

    return SubmenuItem("Inspection", inspect_submenu, menu)