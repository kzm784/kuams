# kuams 🐧
ROS 2 package for KUAMS (Kansai University Autonomous Measurement System)

<img src="./docs/kuams.png">

## Requirements
- Ubuntu 22.04 
- ROS2 humble
- [ros2_whill](https://github.com/kzm784/ros2_whill.git)
- [ros2_whill_interfaces (crystal-devel)](https://github.com/WHILL/ros2_whill_interfaces)
- [Livox-SDK2](https://github.com/Livox-SDK/Livox-SDK2)
- [livox_ros_driver2](https://github.com/Livox-SDK/livox_ros_driver2.git)
- [waypoint_manager](https://github.com/kzm784/waypoint_manager.git)
- [lidar_localization_ros2](https://github.com/kzm784/lidar_localization_ros2.git)


## Build
please install before building
```sh
sudo apt install ros-humble-navigation2
sudo apt install ros-humble-velodyne

```
In your shell:
```sh
cd ~/<your_ros2_ws>/src
git clone https://github.com/kzm784/kuams.git
cd ~/<your_ros2_ws>
colcon build 
source install/setup.bash
