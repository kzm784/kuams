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


    return LaunchDescription([
        laser_filter_node
    ])
