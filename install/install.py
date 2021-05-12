import json
import os

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
            