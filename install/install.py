import json
import os

class RobotPackageInstaller():
    def __init__(self, commands="shellscripts.json", variables="variables.json", playbooks="rover_models.json"):
        
        # loads all possible install commands
        with open(commands, "r") as inputfile:
            self.install_commands = json.load(inputfile)

        # load all versioned variables
        with open(variables, "r") as inputfile:
            self.variables = json.load(inputfile)

        # load all model-specific install "playbook"
        with open(playbooks, "r") as inputfile:
            self.playbooks = json.load(inputfile)

    def set_model(self, model:str):
        if model not in self.playbooks:
            raise ValueError("Invalid robot model %s. No valid plan to install for %s" % (model, model))
        
        self.model = model


    def run_install(self, logfile_location):
        for play in self.playbooks[]



with open("shellscripts.json", "r") as inputfile:
    data = json.load(inputfile)

with open("variables.json", "r") as inputfile:
    variables = json.load(inputfile)

def replace_matched_variables(command):
    for var in variables:
        if var in command:
            command = command.replace(var, variables[var])

    return command

for key in data:
    for command_set in data[key]:
        for command_category, commands in command_set.items():
            print('DOING %s PART OF INSTALLATION' % command_category)
            
            if isinstance(commands, list):
                for command in commands:
                    command = replace_matched_variables(command)
                    print(command)
            else:
                command = replace_matched_variables(commands)
                print(command)

            print('SUCCESS!')
            print('')
            