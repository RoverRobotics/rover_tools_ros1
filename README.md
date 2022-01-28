# rover_tools

Rover Tools are a new set of tools to help users quickly and easily install the required software to run a Rover robot. Rover tools are targetted for provisioning Ubuntu.

# install

The first time you run rover tools run these commands to install necessary dependancies

```
cd ~/
git clone https://github.com/roverrobotics/rover_tools -b 1.1.1
cd ~/rover_tools
./install.sh
```

# usage

```
cd ~/rover_tools
./start.sh
```

## Menu Options

<ol>
  <li>Install
    <ol>
    <li>pro_ros1</li>
    <li>zero2_ros1</li>
    <li>mini_ros1</li>
    <li>pro2_ros1</li>
    <li>Return to Rover Tools</li>
    </ol>
  </li>
  <li>Calibrate
    <ol>
    <li>pro_2WD_ros1</li>
    <li>pro_4WD_ros1</li>
    <li>zero2_2WD_ros1</li>
    <li>zero2_4WD_ros1</li>
    <li>pro2_2WD_ros1</li>
    <li>mini_2WD_ros1</li>
    <li>Return to Rover Tools</li>
    </ol>
  </li>
  <li>Test
    <ol>
    <li>pro_2WD_ros1</li>
    <li>pro_4WD_ros1</li>
    <li>zero2_2WD_ros1</li>
    <li>zero2_4WD_ros1</li>
    <li>pro2_2WD_ros1</li>
    <li>mini_2WD_ros1</li>
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
