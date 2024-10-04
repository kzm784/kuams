from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory, get_package_share_path
import yaml

def generate_launch_description():

    # HLDS Laser Node
    hlds_port = LaunchConfiguration('hlds_port', default='/dev/hlds')
    hlds_frame_id = LaunchConfiguration('hlds_frame_id', default='laser')

    hlds_laser_node = Node(
        package='hls_lfcd_lds_driver',
        executable='hlds_laser_publisher',
        name='hlds_laser_publisher',
        parameters=[{'port': hlds_port, 'frame_id': hlds_frame_id}],
        output='screen',
        remappings=[('scan', 'hldsscan')]
    )

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

    # Laser Filters Node
    laser_filter_config_path = os.path.join(get_package_share_path('kuams_bringup'), 'config', 'box_filter.yaml')
    laser_filter_node = Node(
        package='laser_filters',
        executable='scan_to_scan_filter_chain',
        parameters=[laser_filter_config_path],
        remappings=[('scan', 'hldsscan')]
    )

    # Include laserscan_multi_merger.launch.py at the end
    ira_laser_tools_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ira_laser_tools'), 'launch', 'laserscan_multi_merger.launch.py')
        )
    )

    return LaunchDescription([
        hlds_laser_node,
        velodyne_driver_node,
        velodyne_transform_node,
        velodyne_laserscan_node,
        laser_filter_node,
        ira_laser_tools_launch
    ])
