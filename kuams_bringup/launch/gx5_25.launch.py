import os

import ament_index_python

from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node, SetRemap

# Path to the launch files and directories that we will use
_MICROSTRAIN_LAUNCH_FILE = os.path.join(ament_index_python.packages.get_package_share_directory('microstrain_inertial_driver'), 'launch', 'microstrain_launch.py')
_GX5_25_PARAMS_FILE = os.path.join(ament_index_python.packages.get_package_share_directory('kuams_bringup'), 'config', 'gx5_25.yaml')

def generate_launch_description():
  return LaunchDescription([
    # Microstrain node
    IncludeLaunchDescription(
      PythonLaunchDescriptionSource(_MICROSTRAIN_LAUNCH_FILE),
      launch_arguments={
        'configure': 'true',
        'activate': 'true',
        'params_file': _GX5_25_PARAMS_FILE,
        'namespace': '/',
      }.items()
    ),
  ])
