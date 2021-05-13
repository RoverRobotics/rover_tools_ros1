from abc import get_cache_token
import json
import os
import subprocess
import pexpect
import sys
class RobotPackageInstaller():
    def __init__(self, commands="shellscripts.json", variables="variables.json", playbooks="playbooks.json"):

        # loads all possible install commands
        with open(commands, "r") as inputfile:
            self.install_commands = json.load(inputfile)

        # load all versioned variables
        with open(variables, "r") as inputfile:
            self.variables = json.load(inputfile)

        # load all model-specific install "playbook"
        with open(playbooks, "r") as inputfile:
            self.playbooks = json.load(inputfile)

    def set_model(self, model: str):
        if model not in self.playbooks:
            raise ValueError(
                "Invalid robot model %s. No valid plan to install for %s" % (model, model))

        self.model = model

    def replace_matched_variables(self, command):
        for var in self.variables:
            if var in command:
                command = command.replace(var, self.variables[var])
        return command

    def run_install(self, logfile_location="test.log"):
        password = input("Please enter your password: ")
        print ("finished waiting")
        robotscript = pexpect.spawn("/bin/bash" ,encoding='UTF-8',echo = True)
        fout = open(logfile_location,'wb')
        # robotscript.logfile = fout
        robotscript.logfile = sys.stdout
        # robotscript.logfile_read = sys.stdout
        robotscript.sendline("sudo -s")
        robotscript.expect("password", timeout=2)
        robotscript.sendline(password)
        for play in self.playbooks[self.model]:
            for command_set in self.install_commands[play]:
                for command_category, commands in command_set.items():
                    # print('DOING %s PART OF INSTALLATION' %
                    #         command_category)

                    if isinstance(commands, list):
                        for command in commands:
                            command = self.replace_matched_variables(
                                command)
                            # print(command)
                            try:
                                # print("attempting command %s" % command)
                                robotscript.sendline(command)
                                # robotscript.sendline(command.encode(encoding='UTF-8'))
                                # print (robotscript.before + robotscript.after)
                                # robotscript.expect(">")
                            except (SystemError, FileNotFoundError):
                                print ("Failed to run this bash command: %s" % command);

                    else:
                        command = self.replace_matched_variables(
                            commands)
                        # print(command)


if __name__ == "__main__":
    install = RobotPackageInstaller()
    install.set_model('test')
    install.run_install()
# for key in data:
#     for command_set in data[key]:
#         for command_category, commands in command_set.items():
#             print('DOING %s PART OF INSTALLATION' % command_category)

#             if isinstance(commands, list):
#                 for command in commands:
#                     command = replace_matched_variables(command)
#                     print(command)
#             else:
#                 command = replace_matched_variables(commands)
#                 print(command)

#             print('SUCCESS!')
#             print('')
