from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os
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

    # Livox Node
    livox_ros_driver2_node = Node(
        package='livox_ros_driver2',
        executable='livox_ros_driver2_node',
        name='livox_ros_driver2',
        output='screen',
        parameters=[
            {
                'xfer_format': 0,
                'multi_topic': 0,
                'data_src': 0,
                'publish_freq': 10.0,
                'output_data_type': 0,
                'frame_id': 'livox_frame',
                'lvx_file_path': '',
                'user_config_path': os.path.join(
                    bringup_dir, 'config', 'MID360_config.json'
                ),
                'cmdline_input_bd_code': 'livox0000000001',
            }
        ]
    )

    # Realsense Node
    realsense_config_file = os.path.join(bringup_dir, 'config', 'realsense_d435i.yaml')
    realsense_camera_node = Node(
        package='realsense2_camera',
        executable='realsense2_camera_node',
        name='realsense_camera_node',
        namespace='camera',
        output='screen',
        parameters=[realsense_config_file]
    )    

    # Pointcloud to LaserScan Node
    pointcloud_to_laserscan_node = Node(
        package='pointcloud_to_laserscan',
        executable='pointcloud_to_laserscan_node',
        name='pointcloud_to_laserscan',
        remappings=[('cloud_in', 'livox/lidar'),
                    ('scan', '/livox_scan')],
        parameters=[{
            'target_frame': 'livox_frame',
            'transform_tolerance': 0.01,
            'min_height': -0.2,
            'max_height': 0.2,
            'angle_min': -3.1415,
            'angle_max': 3.1415,
            'angle_increment': 0.0087,
            'scan_time': 0.3333,
            'range_min': 0.45,
            'range_max': 30.0,
            'use_inf': True,
            'inf_epsilon': 1.0
        }]
    )

    return LaunchDescription([
        velodyne_driver_node,
        velodyne_transform_node,
        velodyne_laserscan_node,
        livox_ros_driver2_node,
        # realsense_camera_node,
        pointcloud_to_laserscan_node
    ])
