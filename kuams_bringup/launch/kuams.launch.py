import os
import xacro
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    kuams_urdf_path = os.path.join(get_package_share_directory('kuams_description'), 'urdf', 'kuams.xacro')
    kuams_bringup_dir = get_package_share_directory('kuams_bringup')

    declare_param_file_cmd = DeclareLaunchArgument(
        'params',
        default_value=os.path.join(
            kuams_bringup_dir, 'config', 'whill_param.yaml'),
        description='Full path to the ros2 whill param file to use'
    )

    doc =xacro.process_file(kuams_urdf_path)
    robot_desc=doc.toprettyxml(indent='  ')
    f=open(kuams_urdf_path,'w')
    f.write(robot_desc)
    f.close()

    robot_model_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'robot_description': robot_desc}],
        remappings=[('/joint_states', '/whill/joint_states')]
    )

    whill_node = Node(
        package='whill_driver',
        executable='whill',
        name='whill',
        parameters=[LaunchConfiguration('params')],
        remappings=[('/whill/odom', '/odom')]
    )
    
    # Create the launch description and populate
    ld = LaunchDescription()

    # Add launch arguments to the launch description of node
    ld.add_action(declare_param_file_cmd)
    ld.add_action(robot_model_node)
    ld.add_action(whill_node)
    ld.add_action(
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(kuams_bringup_dir, 'launch', 'utils', 'sensors.launch.py'))
        ),
    )    
    # ld.add_action(
    #     IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource(os.path.join(kuams_bringup_dir, 'launch', 'velodyne-all-nodes-VLP16-launch.py'))
    #     ),
    # )
    # ld.add_action(
    #     IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource(os.path.join(kuams_bringup_dir, 'launch', 'hlds_laser.launch.py'))
    #     ),
    # )
    # ld.add_action(
    #     IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource(os.path.join(kuams_bringup_dir, 'launch', 'gx5_25.launch.py'))
    #     ),
    # )
    # ld.add_action(
    #     IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource(os.path.join(kuams_bringup_dir, 'launch', 'static_transform_publisher.launch.py'))
    #     ),
    # )
    # ld.add_action(
    #     IncludeLaunchDescription(
    #         PythonLaunchDescriptionSource(os.path.join(kuams_bringup_dir, 'launch', 'ekf.launch.py'))
    #     ),
    # )

    return ld
