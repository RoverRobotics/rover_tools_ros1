from abc import get_cache_token
import json
import os, stat
from subprocess import PIPE, Popen
import sys
class RobotPackageInstaller():
    def __init__(
        self, 
        commands=(os.path.dirname(__file__) + "/shellscripts.json"), 
        variables=(os.path.dirname(__file__) + "/variables.json"), 
        playbooks=(os.path.dirname(__file__) + "/playbooks.json")
    ):

        # loads all possible install commands
        with open(commands, "r") as inputfile:
            self.install_commands = json.load(inputfile)

        # load all versioned variables
        with open(variables, "r") as inputfile:
            self.variables = json.load(inputfile)

        # load all model-specific install "playbook"
        with open(playbooks, "r") as inputfile:
            self.playbooks = json.load(inputfile)

        # find the verification filepath
        for var in self.variables:
            if "VERIFICATION_FILE" in var:
                self.verification_file_path = self.variables[var]
                self.verification_file_path = (
                    os.path.expanduser("~") + self.verification_file_path.replace("~", "")
                ) if "~" in self.verification_file_path else self.verification_file_path


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

    def get_models(playbooks=(os.path.dirname(__file__) + "/playbooks.json")):
        with open(playbooks, "r") as playbook_file:
            models = json.load(playbook_file).keys()
        return models
            
    
    def run_install(self, logfile_location=os.path.dirname(__file__) + "/install.log", model=None, verification_file_header=None):
        if model is not None:
            self.set_model(model)
        
        # open a master install log
        fout = open(logfile_location,'wb')
        fout.close()

        # clear the verification file and write any valid header
        vout = open(self.verification_file_path, 'w')
        if isinstance(verification_file_header, str):
            vout.write(verification_file_header + '\n')
        vout.close()

        # validate that the playbooks contain valid plays
        try:
            for play in self.playbooks[self.model]:
                for command_set in self.install_commands[play]:
                    pass
        except Exception as e:
            input("there was an error in the .json install configurations. Check playbooks.json and try again: %s " % e)
            exit()
        

        for index ,play in enumerate(self.playbooks[self.model]):
            print("Running install set %d of %d" % (index+1, len(self.playbooks[self.model])), end=" ")
            for command_set in self.install_commands[play]:
                for command_category, commands in command_set.items():
                    fout = open(logfile_location,'a')
                    fout.write("#Bash command \r\n") 
                    if isinstance(commands, list):
                        with open("temp.sh", "w") as temp_bash:
                            for command in commands:
                                command = self.replace_matched_variables(command)
                                temp_bash.write(command+'\n')
                                fout.write(command + "\r\n")

                    else:
                        with open("temp.sh", "w") as temp_bash:
                            command = self.replace_matched_variables(commands)
                            temp_bash.write(command+'\n')
                            fout.write(command + "\r\n")

                    print(".", end="")
                    fout.write("#Terminal Output \r\n")
                    os.chmod("temp.sh", stat.S_IROTH | stat.S_IWOTH | stat.S_IXOTH | stat.S_IRUSR | stat.S_IWUSR |  stat.S_IXUSR)
                    output = Popen("%s" % ("/bin/bash temp.sh"), shell=True, stdout=PIPE, stderr=PIPE)
                    stdout, stderr = output.communicate()
                    stdout = str(stdout.decode('UTF-8')).replace("\n", "\r\n")
                    stderr = str(stderr.decode('UTF-8')).replace("\n", "\r\n")

                    fout.write(stdout)
                    fout.write(stderr)
                    self.verify_last_()
            print("")

    def verify_last_(self):
        # the expectation is that there is a verification file which
        # has 1 line per install operation having the work Success or Failure
        with open(self.verification_file_path, "r") as verification_file:
            lines = verification_file.readlines()
            if len(lines) > 0:
                if "Fail" in lines[-1] or "fail" in lines[-1]:
                    input("Installer failed to perform %s" % lines[-1])

    def print_verification_results(self):
        if self.verification_file_path is not None:
            with open(self.verification_file_path, "r") as vf:
                lines = vf.readlines()
                for line in lines:
                    print(line, end="")

    def get_verification_file(self):
        if self.verification_file_path is not None:
            return self.verification_file_path
        else:
            return None