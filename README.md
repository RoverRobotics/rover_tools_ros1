# rover_tools

Rover Tools are a new set of tools to help users quickly and easily install the required software to run a Rover robot. Rover tools are targeted for Ubuntu 20.04 LTS. You must install ROS Noetic before running the setup script, follow these instructions for the easiest installation - http://wiki.ros.org/ROS/Installation/TwoLineInstall

# install

The first time you run rover tools run these commands to install necessary dependancies

```
cd ~/
git clone https://github.com/roverrobotics/rover_tools_ros1
cd ~/rover_tools_ros1
./start.sh
```

# usage

```
cd ~/rover_tools_ros1
./start.sh
```

** To install the mini or MĪTI version you will need to power on your robot and connect it to the computer running the script via the USB cable. **

## Menu Options

<ol>
  <li>Install
    <ol>
    <li>pro_ros1</li>
    <li>zero2_ros1</li>
    <li>Return to Rover Tools</li>
    </ol>
  </li>
  <li>Calibrate
    <ol>
    <li>pro_2WD_ros1</li>
    <li>pro_4WD_ros1</li>
    <li>zero2_2WD_ros1</li>
    <li>zero2_4WD_ros1</li>
    <li>Return to Rover Tools</li>
    </ol>
  </li>
  <li>Test
    <ol>
    <li>pro_2WD_ros1</li>
    <li>pro_4WD_ros1</li>
    <li>zero2_2WD_ros1</li>
    <li>zero2_4WD_ros1</li>
    <li>Return to Rover Tools</li>
    </ol>
  </li>
  <li>Exit</li>
</ol>

# Troubleshooting
If the install script has failed, view the detailed log by running the following command

```
cat ~/rr-install-verification.file
```

Here is a sample output of a failure <br>
![image](https://user-images.githubusercontent.com/6597441/128610405-4e99d424-48ff-4ce5-9775-ebf714dda4d8.png)

You can then look in rover_tools/install/shellscripts.json to view the command that caused the failure
