import json
import os
import subprocess
from subprocess import PIPE, Popen
import sys
import stat

TEMP_SHELL_SCRIPT_LOC = (os.path.dirname(__file__) + "/temp.sh")

def get_models(
    setup_commands_file=(os.path.dirname(__file__) + "/setup_shellscripts.json")
):
    # load commands
    with open(setup_commands_file, "r") as inputfile:
        commands = json.load(inputfile)

    # these are the models 
    return commands.keys()


def launch_robot_mode(
    model:str,
    mode="normal",
    setup_commands_file=(os.path.dirname(__file__) + "/setup_shellscripts.json"),
):
    # load commands
    with open(setup_commands_file, "r") as inputfile:
        commands = json.load(inputfile)

    if model in commands:
        if mode in commands[model]:  
            build_shell_script(commands[model][mode])
            run_shell_script()
        else:
            raise ValueError('attempted to put the robot into an unknown mode: %s' % mode)
    else:
        raise ValueError('invalid robot model. could not setup model: %s' % model)

def build_shell_script(commands, loc=TEMP_SHELL_SCRIPT_LOC):
    if isinstance(commands, list):
        with open(loc, "w") as temp_bash:
            for command in commands:
                temp_bash.write(command + '\n')
    else:
        with open(loc, "w") as temp_bash:
            temp_bash.write(commands + '\n')


def run_shell_script(loc=TEMP_SHELL_SCRIPT_LOC):
    os.chmod(loc, stat.S_IROTH | stat.S_IWOTH |
                             stat.S_IXOTH | stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR)
    output = Popen("/bin/bash %s" % loc,
                    shell=True, stdout=PIPE, stderr=PIPE)
    stdout, stderr = output.communicate()
    stdout = str(stdout.decode('UTF-8')).replace("\n", "\r\n")
    stderr = str(stderr.decode('UTF-8')).replace("\n", "\r\n")
    return stdout, stderr