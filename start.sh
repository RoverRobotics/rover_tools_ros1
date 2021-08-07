cwd=$(pwd)
cf="${cwd}/../credentials.json"
python3 ~/rover_tools/menu/menu_main.py --cf ${cf}
source /opt/ros/melodic/setup.bash
source ~/catkin_ws/devel/setup.bash
