# kuams 🐧
ROS 2 package for KUAMS (Kansai University Autonomous Measurement System)

## Requirements
- Ubuntu 22.04 
- ROS2 humble
- [ros2_whill](https://github.com/kzm784/ros2_whill.git)
- [ros2_whill_interfaces (crystal-devel)](https://github.com/WHILL/ros2_whill_interfaces)
- [velodyne (humble-devel)](https://github.com/ros-drivers/velodyne.git)


## Build
In your shell:
```sh
cd ~/<your_ros2_ws>/src
git clone https://github.com/kzm784/kuams.git
cd ~/<your_ros2_ws>
colcon build 
source install/setup.bash