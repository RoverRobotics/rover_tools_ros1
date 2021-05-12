import pexpect
import sys
import boto3
#import os
password = "will"
print("Running")
child = pexpect.spawn ('bash')
child.logfile = sys.stdout.buffer
child.sendline("sudo apt-get update")
child.expect("password")
child.sendline(password)
child.sendline('sudo usermod -aG dialout,sudo,input $USER')
child.sendline('groups $USER')
i = child.expect(['dialout', 'sudo', '[#\$] '])
ros = '''sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' '''
child.sendline(ros)
child.sendline(''' sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 ''')
print(child.after)