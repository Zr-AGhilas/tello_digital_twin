from setuptools import find_packages, setup

package_name = 'tello_twin_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aghilas',
    maintainer_email='aghilas@todo.todo',
    description='Control and dynamics nodes for Tello digital twin',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cmd_test = tello_twin_control.cmd_test:main',
            'simple_dynamics = tello_twin_control.simple_dynamics:main',
            'gazebo_pose_sender = tello_twin_control.gazebo_pose_sender:main',
            'gz_pose_relay = tello_twin_control.gz_pose_relay:main',
        ],
    },
)
