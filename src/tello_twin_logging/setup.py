from setuptools import find_packages, setup

package_name = 'tello_twin_logging'

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
    description='Tello twin logging nodes',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'logger_node = tello_twin_logging.logger_node:main',
        ],
    },
)
