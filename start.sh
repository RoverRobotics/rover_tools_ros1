#!/bin/bash
sudo apt-get update
sudo apt-get install python-pip -y
sudo apt-get install python3-pip -y
sudo apt-get install screen -y
sudo apt-get install nano -y
sudo apt install cmake -y
sudo apt install git -y 
sudo apt install nano -y
sudo apt install net-tools -y
sudo apt install openssh-server -y
sudo apt-get install python3-rostopic python3-rosdep python3-rosinstall python3-rosinstall-generator python3-wstool build-essential ros-noetic-serial ros-noetic-joy ros-noetic-twist-mux ros-noetic-tf2-geometry-msgs ros-noetic-robot-localization ros-noetic-gmapping ros-noetic-move-base -y
pip3 install console-menu
pip3 install boto3
pip3 install pexpect
pip install six
cp -rf ../rover_tools_ros1 ~/
git clone https://github.com/roverrobotics/robottests ~/rover_tools_ros1/testing/robottests/
cwd=$(pwd)
cf="${cwd}/../credentials.json"
python3 ~/rover_tools_ros1/menu/menu_main.py --cf ${cf}
source /opt/ros/noetic/setup.bash
source ~/catkin_ws/devel/setup.bash
