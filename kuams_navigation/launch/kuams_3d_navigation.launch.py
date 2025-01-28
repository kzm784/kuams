import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    navigation_data_dir = os.getenv('NAVIGATION_DATA_DIR')
    navigation_data_name = os.getenv('NAVIGATION_DATA_NAME')
    nav2_map_path = os.path.join(
        navigation_data_dir,
        navigation_data_name,
        f"{navigation_data_name}.yaml"
    )

    # Declare arguments #
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    params_file = LaunchConfiguration('params_file')
    rviz2_file = LaunchConfiguration('rviz2_file')

    declare_arg_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(
            get_package_share_directory('kuams_navigation'),
            'config',
            'kuams_nav2_3d_params.yaml'),
        description='The full path to the param file.'
    )

    declare_arg_rviz2_config_path = DeclareLaunchArgument(
        'rviz2_file', default_value=os.path.join(
            get_package_share_directory('kuams_navigation'),
            'rviz',
            '3d_nav2_view.rviz'),
        description='The full path to the rviz file'
    )

    nav2_launch_file_dir = os.path.join(
        get_package_share_directory('kuams_navigation'),
        'launch',
        'utils'
    )

    nav2_collision_monitor_launch_file_dir = os.path.join(
        get_package_share_directory('nav2_collision_monitor'), 'launch'
    )

    # Launch files and Nodes #
    nav2_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            nav2_launch_file_dir, '/bringup_launch.py']),
        launch_arguments={
            'map': nav2_map_path,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
        }.items(),
    )

    rviz2_node = Node(
        name='rviz2',
        package='rviz2', executable='rviz2', output='screen',
        arguments=['-d', rviz2_file],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    # nav2_collision_monitor
    collision_monitor_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [nav2_collision_monitor_launch_file_dir, '/collision_monitor_node.launch.py']),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'params_file': params_file
        }.items(),
    )

    ld = LaunchDescription()
    ld.add_action(declare_arg_params_file)
    ld.add_action(declare_arg_rviz2_config_path)

    ld.add_action(nav2_node)
    ld.add_action(rviz2_node)
    ld.add_action(collision_monitor_launch)

    return ld
