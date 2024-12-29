from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory, get_package_share_path
import yaml

def generate_launch_description():

    bringup_dir = get_package_share_directory("kuams_bringup")

    # Velodyne Nodes
    driver_share_dir = get_package_share_directory('velodyne_driver')
    driver_params_file = os.path.join(driver_share_dir, 'config', 'VLP16-velodyne_driver_node-params.yaml')
    velodyne_driver_node = Node(
        package='velodyne_driver',
        executable='velodyne_driver_node',
        output='both',
        parameters=[driver_params_file]
    )

    convert_share_dir = get_package_share_directory('velodyne_pointcloud')
    convert_params_file = os.path.join(convert_share_dir, 'config', 'VLP16-velodyne_transform_node-params.yaml')
    with open(convert_params_file, 'r') as f:
        convert_params = yaml.safe_load(f)['velodyne_transform_node']['ros__parameters']
    convert_params['calibration'] = os.path.join(convert_share_dir, 'params', 'VLP16db.yaml')
    velodyne_transform_node = Node(
        package='velodyne_pointcloud',
        executable='velodyne_transform_node',
        output='both',
        parameters=[convert_params]
    )

    laserscan_share_dir = get_package_share_directory('velodyne_laserscan')
    laserscan_params_file = os.path.join(laserscan_share_dir, 'config', 'default-velodyne_laserscan_node-params.yaml')
    velodyne_laserscan_node = Node(
        package='velodyne_laserscan',
        executable='velodyne_laserscan_node',
        output='both',
        parameters=[laserscan_params_file]
    )

    # Include pointcloud_to_laser_scan
    pointcloud_to_laserscan_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('pointcloud_to_laserscan'), 'launch', 'sample_pointcloud_to_laserscan_launch.py')
        )
    )

    # Include rviz_MID660_launch.py from livox_ros_driver2 with custom user_config_path
    livox_driver_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('livox_ros_driver2'), 'launch_ROS2', 'rviz_MID360_launch.py')
        ),
        launch_arguments={
            'user_config_path': os.path.join(
                get_package_share_directory('kuams_bringup'),
                'config',
                'MID360_config.json'
            )
        }.items()
    )

    livox_ros_driver2_node = Node(
        package="livox_ros_driver2",
        executable="livox_ros_driver2_node",
        name="livox_ros_driver2",
        output="screen",
        parameters=[
            {
                "xfer_format": 0,
                "multi_topic": 0,
                "data_src": 0,
                "publish_freq": 10.0,
                "output_data_type": 0,
                "frame_id": "livox_frame",
                "lvx_file_path": "",
                "user_config_path": os.path.join(
                    bringup_dir, "config", "MID360_config.json"
                ),
                "cmdline_input_bd_code": "livox0000000001",
            }
        ]

    )


    
    return LaunchDescription([
        velodyne_driver_node,
        velodyne_transform_node,
        velodyne_laserscan_node,
        pointcloud_to_laserscan_launch,
        # livox_driver_launch
        livox_ros_driver2_node
    ])
