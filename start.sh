#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
pip3 install console-menu
pip3 install boto3
python3 menu/menu_main.py
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
