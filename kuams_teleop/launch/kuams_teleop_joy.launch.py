from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    package_name = 'kuams_teleop'
    config_file_path = os.path.join(
        get_package_share_directory(package_name),
        'config',
        'config_kuams_teleop.yaml'
    )

    return LaunchDescription([
        Node(
            package='joy',
            executable='joy_node',
            name='joy_node',
            output='screen',
            parameters=[{
                'deadzone': 0.1,
                'autorepeat_rate': 20.0
            }],
            remappings=[
                ('joy', '/whill/controller/joy')
            ],
        ),
    ])
