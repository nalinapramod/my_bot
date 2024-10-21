import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    # Declare the use_sim_time argument
    use_sim_time = LaunchConfiguration('use_sim_time', default='false')

    # Set the path to the xacro file and the inertial macros file
    pkg_path = os.path.join(get_package_share_directory('my_bot'))
    xacro_file = os.path.join(pkg_path, 'description', 'robot.urdf.xacro')
    
    # Process the xacro file
    robot_description_config = xacro.process_file(xacro_file)

    # Set the robot description parameters
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}

    # Define the robot_state_publisher node
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )

    # Return the launch description with the necessary nodes
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'
        ),
        node_robot_state_publisher
    ])

