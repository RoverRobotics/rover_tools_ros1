import os
import json
from shared.utils import user_says_yes


class ManualInspection():
    def __init__(self, inspection_file=(os.path.dirname(__file__) + "/inspection.json")):
        with open(inspection_file, "r") as f:
            self.inspection_procedure = json.load(f)
        self.results = {}
    
    def get_models(self):
        return self.inspection_procedure.keys()

    def run_inspection(self, model):

        self.results = {}
        if model not in self.get_models():
            raise ValueError("cannot run inspection for %s: invalid model" % model)

        for inspection_task in self.inspection_procedure[model]:
            
            # pass fail type question
            if isinstance(inspection_task["Specification"], bool):
                if user_says_yes(inspection_task["Description"]):
                    self.results[inspection_task["Description"]] = "Pass"
                else:
                    self.results[inspection_task["Description"]] = "Fail"

            # range type question
            elif isinstance(inspection_task["Specification"], list):
                print(inspection_task["Description"])
                print('acceptable range: ', inspection_task["Specification"])
                user_value = float(input('actual: '))
                if inspection_task["Specification"][0] < user_value and user_value < inspection_task["Specification"][1]:
                    self.results[inspection_task["Description"]] = "Pass"
                else:
                    self.results[inspection_task["Description"]] = "Fail"

            # single value type question
            elif isinstance(inspection_task["Specification"], int) or isinstance(inspection_task["Specification"], float):
                print(inspection_task["Description"])
                print('expected value: ', inspection_task["Specification"])

                user_value = float(input('actual: '))
                if user_value == inspection_task["Specification"]:
                    self.results[inspection_task["Description"]] = "Pass"
                else:
                    self.results[inspection_task["Description"]] = "Fail"
            else:
                raise ValueError('Unknown type for specification: %s' % inspection_task["Specification"])

            print('')

        return self.results




