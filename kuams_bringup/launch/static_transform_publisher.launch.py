from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([

        # Velodyne
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='velodyne_static_transform_publisher',
            output='screen',
            arguments=[
                "--x", "0.1",
                "--y", "0",
                "--z", "0.8",
                "--roll", "0",
                "--pitch", "0",
                "--yaw", "0",
                "--frame-id", "base_link",
                "--child-frame-id", "velodyne"
            ]
        ),

        # Laser
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='laser_static_transform_publisher',
            output='screen',
            arguments=[
                "--x", "0.5",
                "--y", "0",
                "--z", "0.4",
                "--roll", "3.1415926535",
                "--pitch", "0",
                "--yaw", "0",
                "--frame-id", "base_link",
                "--child-frame-id", "laser"
            ]
        ),
        
        # 3dm-gx5-25 IMU
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            output='screen',
            arguments=[
                "--x", "0.1",
                "--y", "0",
                "--z", "0.75",
                "--roll", "0",
                "--pitch", "0",
                "--yaw", "0",
                "--frame-id", "base_link",
                "--child-frame-id", "gx5_25"
            ]
        ),
    ])
