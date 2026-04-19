from setuptools import setup
import os
from glob import glob

package_name = 'tello_twin_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='aghilas',
    maintainer_email='aghilas@todo.todo',
    description='Tello twin bringup package',
    license='MIT',
    tests_require=['pytest'],
)
