#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
sudo apt-get install screen -y
pip3 install console-menu
pip3 install boto3
pip3 install pexpect
cp -r ../rover_tools ~/
python3 ~/rover_tools/menu/menu_main.py
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
