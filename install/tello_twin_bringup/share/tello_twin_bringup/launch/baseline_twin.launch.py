from launch import LaunchDescription
from launch.actions import ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():
    world_path = '/home/aghilas/tello_twin_ws/src/tello_twin_bringup/worlds/simple_drone_world.sdf'
    gazebo = ExecuteProcess(
        cmd=['gz', 'sim', '-r', world_path],
        output='screen'
    )

    return LaunchDescription([
        gazebo,

        Node(
            package='tello_twin_control',
            executable='cmd_test',
            name='cmd_test',
            output='screen'
        ),
        Node(
            package='tello_twin_control',
            executable='simple_dynamics',
            name='simple_dynamics',
            output='screen'
        ),
        Node(
            package='tello_twin_logging',
            executable='logger_node',
            name='logger_node',
            output='screen'
        ),
        Node(
            package='tello_twin_control',
            executable='gazebo_pose_sender',
            name='gazebo_pose_sender',
            output='screen'
        ),
        Node(
            package='tello_twin_control',
            executable='gz_pose_relay',
            name='gz_pose_relay',
            output='screen'
        ),
    ])
