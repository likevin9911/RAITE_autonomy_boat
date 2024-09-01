# autonomy_boat_sim

This repository is the home to the source code and software documentation for MTU's USV simulation environment, which is forked from the VRX simulation. 
* This project includes the MTU pontoon USV model and the map of the sunken city. 

## Environment Information
  - Operating System: Ubuntu 20.04 LTS
  - ROS Version: ROS 1 Noetic

## Install Prerequisites
1. First, I recommend upgrading the packages installed on your system:
```
sudo apt update
sudo apt full-upgrade
```
2. Setup the relevant repo and install dependencies:
```
sudo apt install -y build-essential cmake cppcheck curl git gnupg libeigen3-dev libgles2-mesa-dev lsb-release pkg-config protobuf-compiler qtbase5-dev python3-dbg python3-pip python3-venv ruby software-properties-common wget 
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
sudo sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list'
wget http://packages.osrfoundation.org/gazebo.key -O - | sudo apt-key add -
sudo apt update
DIST=noetic
GAZ=gazebo11
sudo apt install ${GAZ} lib${GAZ}-dev ros-${DIST}-gazebo-plugins ros-${DIST}-gazebo-ros ros-${DIST}-hector-gazebo-plugins ros-${DIST}-joy ros-${DIST}-joy-teleop ros-${DIST}-key-teleop ros-${DIST}-robot-localization ros-${DIST}-robot-state-publisher ros-${DIST}-joint-state-publisher ros-${DIST}-rviz ros-${DIST}-ros-base ros-${DIST}-teleop-tools ros-${DIST}-teleop-twist-keyboard ros-${DIST}-velodyne-simulator ros-${DIST}-xacro ros-${DIST}-rqt ros-${DIST}-rqt-common-plugins
```

## Instructions to Setup
"Apologies for the round about way of setting this up"
1. Create a new workspace:
```
mkdir -p ~/raite_ws/src
cd ~/raite_ws/src
```

2. Clone the repository into your workspace:
```
git clone git@github.com:likevin9911/RAITE_autonomy_boat.git
```

3. Once cloned, you should see some extra folders that have nothing in them. Make sure to delete them as they are not part of the package. Only keep the usv_vrx  and vrx folder.
```
rm -rf gazebo_ros_pkgs heron_simulator pcl realsense-ros robot_localization rtabmap_ros slam_gmapping 
```

4. Build your workspace
```
cd ~/raite_ws
catkin_make
```

5. In your home directory, source the setup file by placing this line of code into your .bashrc file and open new terminal.
```
source ~/raite_ws/devel/setup.bash
```

6. Lastly, verify your setup, make sure everything is setup correctly. You should see the 'usv_vrx' and 'vrx' packages listed.
```
rospack list
```

## Debug
If the vrx package is causing too many errors, clone the vrx simulation (gazebo-classic) into your workspace. Here is the wikipage if this method of setting up doesn't work: https://github.com/osrf/vrx/wiki/VRX-Classic-Home
```
cd ~/raite_ws/src
git clone --branch gazebo_classic https://github.com/osrf/vrx.git
```
## Run the simulation
1. After sourcing the simulation, lets try first launching the vrx simulation. Gazebo should be launching the Syndey Regatta with a simple environemnt. Close out once it is running. THIS IS NOT THE MTU boat. 
```
roslaunch vrx_gazebo vrx.launch
```

2. Try running the simulation using our model this time
```
roslaunch usv_gazebo all.launch
```
* This should open up gazebo to the sunken city map and should open up RVIZ.
* If there shows to be too many errors, don't hesistate to contact me at kgli@mtu.edu or submit a request.
```
roslaunch vrx_gazebo usv_keydrive.launch
```
* If you want to move the boat via keyboard.


3. This is a table of where the scripts are located and which to focus on.  
```
convert2gps_sim/convert2gps_mavros.py (raite_ws/src/usv_vrx/usv_navigation/scripts) #converts lidar bounding box position into gps coordinates relative to the velodyne frame. Lidar has a 40% front view, RANSAC and another algorithm is there to tune. 

boat_test.py (raite_ws/src/usv_vrx/usv_navigation/scripts) #launches the connection from jetson to motors and includes the camera topic for its own bbox.
```
We are also in the process of training our Yolov4, our dataset maybe too big to upload to github. Email me if you would like to see our dataset.
