import json
import os
import stat
from subprocess import PIPE, Popen
import sys
from types import ModuleType


class RobotCalibrator():
    def __init__(self, commands=(os.path.dirname(__file__) + "/calibration_shellscripts.json"),
                 playbooks=(os.path.dirname(__file__) + "/calibration_playbook.json")):
        # loads all possible install commands
        with open(commands, "r") as inputfile:
            self.commands = json.load(inputfile)

        # load all model-specific install "playbook"
        with open(playbooks, "r") as inputfile:
            self.playbooks = json.load(inputfile)

    def set_model(self, model: str):
        if model not in self.playbooks:
            raise ValueError(
                "Invalid robot model %s. No valid plan to install for %s" % (model, model))
        self.model = model

    def run_calibration(self):
        print("Running %s calibration" % self.model)

    def calibrate(self, model=None):
        if model is not None:
            self.set_model(model)
            fout = open(logfile_location, 'wb')
            fout.close()

            try:
                for play in self.playbooks[self.model]:
                    for command_set in self.commands[play]:
                        pass
            except Exception as e:
                input(
                    "there was an error in the .json install configurations. Check playbooks.json and try again: %s " % e)
                exit()

            for index, play in enumerate(self.playbooks[self.model]):
                for command_set in self.commands[play]:
                    for command_category, commands in command_set.items():
                        fout = open(logfile_location, 'a')
                        fout.write("#Bash command \r\n")
                        if isinstance(commands, list):
                            with open("temp.sh", "w") as temp_bash:
                                for command in commands:
                                    command = self.replace_matched_variables(
                                        command)
                                    temp_bash.write(command+'\n')
                                    fout.write(command + "\r\n")

                        else:
                            with open("temp.sh", "w") as temp_bash:
                                command = self.replace_matched_variables(
                                    commands)
                                temp_bash.write(command+'\n')
                                fout.write(command + "\r\n")

                        print(".", end="")
                        fout.write("#Terminal Output \r\n")
                        os.chmod("temp.sh", stat.S_IROTH | stat.S_IWOTH |
                                 stat.S_IXOTH | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
                        output = Popen("%s" % ("/bin/bash temp.sh"),
                                       shell=True, stdout=PIPE, stderr=PIPE)
                        stdout, stderr = output.communicate()
                        stdout = str(stdout.decode('UTF-8')
                                     ).replace("\n", "\r\n")
                        stderr = str(stderr.decode('UTF-8')
                                     ).replace("\n", "\r\n")

                        fout.write(stdout)
                        fout.write(stderr)
                        if "setup" in model:
                            self.run_setup()
                print("")
            
            # resume automatically
            # self.set_model(model.replace("setup","resume"))
            # self.run_setup()
        # open a master install log
