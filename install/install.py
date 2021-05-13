from abc import get_cache_token
import json
import os, stat
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
        print ("starting install....")

        # open a master install log
        fout = open(logfile_location,'wb')
        fout.close()

        for play in self.playbooks[self.model]:
            for command_set in self.install_commands[play]:
                for command_category, commands in command_set.items():
                    
                    if isinstance(commands, list):
                        with open("temp.sh", "w") as temp_bash:
                            for command in commands:
                                command = self.replace_matched_variables(command)
                                temp_bash.write(command+'\n')  
                    else:
                        with open("temp.sh", "w") as temp_bash:
                            command = self.replace_matched_variables(commands)
                            temp_bash.write(command+'\n')

                    print(os.getcwd())
                    fout = open(logfile_location,'a')
                    os.chmod("temp.sh", stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH | stat.S_IRUSR | stat.S_IWUSR |  stat.S_IXUSR)
                    os.system("echo %s | %s" % (password, "/bin/bash temp.sh"))


if __name__ == "__main__":
    install = RobotPackageInstaller()
    install.set_model('test')
    install.run_install()
