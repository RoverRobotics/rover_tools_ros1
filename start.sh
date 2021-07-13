#!/bin/bash
sudo apt-get update
sudo apt-get install python3-pip -y
sudo apt-get install screen -y
sudo apt-get install nano -y
pip3 install console-menu
pip3 install boto3
pip3 install pexpect
cp -rf ../rover_tools ~/
git clone https://github.com/roverrobotics/robottests ~/rover_tools/testing/robottests/
cwd=$(pwd)
cf="${cwd}/../credentials.json"
python3 ~/rover_tools/menu/menu_main.py --cf ${cf}
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
