
import os

import launch
import launch.actions
import launch.events

import launch_ros
import launch_ros.actions
import launch_ros.events

from launch import LaunchDescription
from launch.actions import TimerAction
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

import lifecycle_msgs.msg

from ament_index_python.packages import get_package_share_directory

def generate_launch_description():

    kuams_navigation_dir = get_package_share_directory('kuams_navigation')
    rviz_config_dir = os.path.join(kuams_navigation_dir, 'rviz')
    kuams_description_dir = get_package_share_directory('kuams_description')
    rviz_config_file = os.path.join(rviz_config_dir, 'rviz_kuams_navigation.rviz')
    rviz_stylesheet = os.path.join(kuams_description_dir, 'rviz', 'dark.qss')

    ld = LaunchDescription()

    declare_map_pcd = DeclareLaunchArgument(
        'map_path',
        description='Path to the map PCD file.'
    )

    map_pcd_path = LaunchConfiguration('map_path')

    localization_param_dir = launch.substitutions.LaunchConfiguration(
        'localization_param_dir',
        default=os.path.join(
            get_package_share_directory('kuams_navigation'),
            'config',
            'params_lidar_localization_ros2.yaml'))

    lidar_localization = launch_ros.actions.LifecycleNode(
        name='lidar_localization',
        namespace='',
        package='lidar_localization_ros2',
        executable='lidar_localization_node',
        parameters=[localization_param_dir, {
            'map_path': map_pcd_path
        }],
        remappings=[('/cloud','/velodyne_points'),
                    ('/odom', '/odom')],
        output='screen')

    to_inactive = launch.actions.EmitEvent(
        event=launch_ros.events.lifecycle.ChangeState(
            lifecycle_node_matcher=launch.events.matches_action(lidar_localization),
            transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
        )
    )

    from_unconfigured_to_inactive = launch.actions.RegisterEventHandler(
        launch_ros.event_handlers.OnStateTransition(
            target_lifecycle_node=lidar_localization,
            goal_state='unconfigured',
            entities=[
                launch.actions.LogInfo(msg="-- Unconfigured --"),
                launch.actions.EmitEvent(event=launch_ros.events.lifecycle.ChangeState(
                    lifecycle_node_matcher=launch.events.matches_action(lidar_localization),
                    transition_id=lifecycle_msgs.msg.Transition.TRANSITION_CONFIGURE,
                )),
            ],
        )
    )

    from_inactive_to_active = launch.actions.RegisterEventHandler(
        launch_ros.event_handlers.OnStateTransition(
            target_lifecycle_node=lidar_localization,
            start_state = 'configuring',
            goal_state='inactive',
            entities=[
                launch.actions.LogInfo(msg="-- Inactive --"),
                launch.actions.EmitEvent(event=launch_ros.events.lifecycle.ChangeState(
                    lifecycle_node_matcher=launch.events.matches_action(lidar_localization),
                    transition_id=lifecycle_msgs.msg.Transition.TRANSITION_ACTIVATE,
                )),
            ],
        )
    )

    rviz2_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file,
                   '--stylesheet', str(rviz_stylesheet)],
        output='screen')

    delayed_start = TimerAction(
        period=5.0,
        actions=[
            from_unconfigured_to_inactive,
            from_inactive_to_active,
            lidar_localization,
            to_inactive,
        ]
    )

    ld.add_action(declare_map_pcd)
    ld.add_action(rviz2_node)
    ld.add_action(delayed_start)

    return ld
