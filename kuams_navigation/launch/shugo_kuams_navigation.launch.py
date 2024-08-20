import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.actions import PushRosNamespace
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml, ReplaceString


def generate_launch_description():
    # Declare arguments #
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    map_yaml_file = LaunchConfiguration('map')
    params_file = LaunchConfiguration('params_file')
    rviz2_file = LaunchConfiguration('rviz2_file')

    declare_arg_map = DeclareLaunchArgument(
        'map',
        description='The full path to the map yaml file.'
    )

    declare_arg_params_file = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(
            get_package_share_directory('kuams_navigation'),
            'config',
            'nav2.param.yaml'),
        description='The full path to the param file.'
    )

    declare_arg_rviz2_config_path = DeclareLaunchArgument(
        'rviz2_file', default_value=os.path.join(
            get_package_share_directory('kuams_navigation'),
            'rviz',
            'shugo_nav2.rviz'),
        description='The full path to the rviz file'
    )

    nav2_launch_file_dir = os.path.join(
        get_package_share_directory('kuams_navigation'),
        'launch'
    )

    lidar_launch_file_dir = os.path.join(
        get_package_share_directory('lidar_localization_ros2'),
        'launch'
    )

    # Launch files and Nodes #
    nav2_node = GroupAction([

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            nav2_launch_file_dir, '/shugo_nav2_bringup.launch.py']),
        launch_arguments={
            'map': map_yaml_file,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
            # '/odom': '/whill/odom',
            # '/cmd_vel': '/whill/controller/cmd_vel'
            }.items(),
    ),

    IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            nav2_launch_file_dir, '/localization_bringup.launch.py']),
        launch_arguments={
            'map': map_yaml_file,
            'params_file': params_file,
            'use_sim_time': use_sim_time,
            # '/odom': '/whill/odom',
            # '/cmd_vel': '/whill/controller/cmd_vel'
            }.items(),
    ),

    ])

    rviz2_node = Node(
        name='rviz2',
        package='rviz2', executable='rviz2', output='screen',
        arguments=['-d', rviz2_file],
        parameters=[{'use_sim_time': use_sim_time}]
    )

    #lidar_node = IncludeLaunchDescription(
    #    PythonLaunchDescriptionSource([
    #        lidar_launch_file_dir, '/lidar_localization.launch.py']),
    #    launch_arguments={
    #        'map': map_yaml_file,
    #        'params_file': params_file,
    #        'use_sim_time': use_sim_time,
    #        # '/odom': '/whill/odom',
    #        # '/cmd_vel': '/whill/controller/cmd_vel'
    #        }.items(),         
    #)

    ld = LaunchDescription()
    ld.add_action(declare_arg_map)
    ld.add_action(declare_arg_params_file)
    ld.add_action(declare_arg_rviz2_config_path)

    ld.add_action(nav2_node)
    ld.add_action(rviz2_node)
    #ld.add_action(lidar_node)
    return ld
