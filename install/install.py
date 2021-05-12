import json
import os

with open("shellscripts.json", "r") as inputfile:
    data = json.load(inputfile)


for key in data:
    for command_set in data[key]:
        for command_category, commands in command_set.items():
            print('DOING %s PART OF INSTALLATION' % command_category)
            
            if isinstance(commands, list):
                for command in commands:
                    print(command)
            else:
                print(commands)

            print('SUCCESS!')
            print('')
            