import os

import launch
import launch.actions
import launch.events

import launch_ros
import launch_ros.actions
import launch_ros.events

from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from ament_index_python.packages import get_package_share_directory

import lifecycle_msgs.msg


def generate_launch_description():

    navigation_data_dir = os.getenv('NAVIGATION_DATA_DIR')
    navigation_data_name = os.getenv('NAVIGATION_DATA_NAME')
    map_path = os.path.join(
        navigation_data_dir,
        navigation_data_name,
        f"{navigation_data_name}.pcd"
    )

    ld = launch.LaunchDescription()

    lidar_localization = launch_ros.actions.LifecycleNode(
        name='lidar_localization',
        namespace='',
        package='lidar_localization_ros2',
        executable='lidar_localization_node',
        parameters=[{
            'registration_method': "NDT_OMP",
            'score_threshold': 2.0,
            'ndt_resolution': 1.0,
            'ndt_step_size': 0.1,
            'ndt_num_threads': 4,
            'ndt_max_iterations': 35,
            'transform_epsilon': 0.01,
            'voxel_leaf_size': 0.2,
            'scan_max_range': 100.0,
            'scan_min_range': 1.0,
            'scan_period': 0.1,
            'use_pcd_map': True,
            'map_path': map_path,
            'set_initial_pose': True,
            'initial_pose_x': 0.0,
            'initial_pose_y': 0.0,
            'initial_pose_z': 0.0,
            'initial_pose_qx': 0.0,
            'initial_pose_qy': 0.0,
            'initial_pose_qz': 0.0,
            'initial_pose_qw': 1.0,
            'use_odom': False,
            'use_imu': False,
            'enable_debug': True,
            'global_frame_id': "map",
            'odom_frame_id': "odom",
            'base_frame_id': "base_link"
        }],
        remappings=[('/cloud', '/velodyne_points')],
        output='screen'
    )

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
            start_state='configuring',
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

    ld.add_action(from_unconfigured_to_inactive)
    ld.add_action(from_inactive_to_active)
    ld.add_action(lidar_localization)
    ld.add_action(to_inactive)

    return ld
