import pexpect
import sys
import boto3
import json

import os

with open(r'./shellscripts.yaml') as file:

# scripts = yaml.load("./shellscripts.yaml")
print(yaml.dump(yaml.load(document), default_flow_style=False))

//subprocess (shell = true,  "source setup.sh ; env>tmpfile.txt") 

# errorno = os.system("sudo apt-get update")
# check()
# errorno = os.system("sudo usermod -aG dialout,sudo,input $USER")
# check()
# errorno = os.system(''' sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $ (lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' ''')
# check()
# errorno = os.system(''' sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 ''')
# check()
# def start_log():
#     global child
#     child.logfile = open("./mylog", "w")


# def stop_log():
#     global child
#     f = open('./mylog', 'r')
#     for line in f:
#         cleanedLine = line.strip()
#         if cleanedLine:  # is not empty
#             print(cleanedLine)
#     f.close()
#     child.logfile.close


# print("Running")
# child = pexpect.spawn('bash')
# start_log()
# child.send('sudo apt-get update')
# child.expect("password")
# password = input()
# child.send(password)
# child.expect("$ ")
# child.sendline('sudo usermod -aG dialout,sudo,input $ USER')
# child.expect("$ ")
# child.sendline('groups $ USER')
# i = child.expect(['dialout', 'sudo', '$ '])
# ros = '''sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $ (lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' '''
# child.sendline(ros)
# child.expect("$ ")
# child.sendline(
#     ''' sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 ''')
# child.expect("$ ")
# stop_log()
