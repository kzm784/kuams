from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():

    laser_filter_config_path = os.path.join(get_package_share_path('kuams_bringup'), 'config', 'box_filter.yaml')

    laser_filter_node = Node(
        package   = 'laser_filters',
        executable= 'scan_to_scan_filter_chain',
        parameters=[laser_filter_config_path],
        remappings=[('scan', 'hlsdscan')]
    )

    laserscan_multi_merger = Node(
        package='ira_laser_tools',
        namespace='',
        executable='laserscan_multi_merger',
        name='laserscan_multi_merger',
        output='screen',
        parameters=[{
            'destination_frame': 'lidar',
            'cloud_destination_topic': '/merged_cloud',
            'scan_destination_topic': '/scan_multi',
            'laserscan_topics': '/scan_filtered /scan',
            # LIST OF THE LASER SCAN TOPICS TO SUBSCRIBE
            'angle_min': -3.14,
            'angle_max': 3.14,
            'angle_increment': 0.00437,
            'scan_time': 0.0,
            'range_min': 0.1,
            'range_max': 100.0,
        }],
    )

    return LaunchDescription([
        laser_filter_node,
        laserscan_multi_merger
    ])
