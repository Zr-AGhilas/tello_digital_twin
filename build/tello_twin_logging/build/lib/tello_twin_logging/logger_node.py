import csv
import os
from datetime import datetime

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry


class LoggerNode(Node):
    def __init__(self):
        super().__init__('logger_node')

        self.latest_cmd = Twist()
        self.latest_twin = None

        self.gz_x = None
        self.gz_y = None
        self.gz_z = None
        self.gz_qx = None
        self.gz_qy = None
        self.gz_qz = None
        self.gz_qw = None

        self.create_subscription(Twist, '/tello_cmd', self.cmd_callback, 10)
        self.create_subscription(Odometry, '/tello_state', self.twin_callback, 10)
        self.create_subscription(Odometry, '/gazebo_state', self.gz_pose_callback, 10)


        log_dir = os.path.expanduser('~/tello_twin_logs')
        os.makedirs(log_dir, exist_ok=True)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.csv_path = os.path.join(log_dir, f'twin_compare_{timestamp}.csv')

        self.csv_file = open(self.csv_path, 'w', newline='')
        self.writer = csv.writer(self.csv_file)

        self.writer.writerow([
            'time',
            'cmd_fb', 'cmd_lr', 'cmd_ud', 'cmd_yaw',
            'twin_x', 'twin_y', 'twin_z',
            'twin_qx', 'twin_qy', 'twin_qz', 'twin_qw',
            'twin_vx', 'twin_vy', 'twin_vz', 'twin_r',
            'gz_x', 'gz_y', 'gz_z',
            'gz_qx', 'gz_qy', 'gz_qz', 'gz_qw',
        ])

        self.timer = self.create_timer(0.1, self.write_row)
        self.get_logger().info(f'Logging to {self.csv_path}')

    def cmd_callback(self, msg: Twist):
        self.latest_cmd = msg

    def twin_callback(self, msg: Odometry):
        self.latest_twin = msg

    def gz_pose_callback(self, msg: Odometry):
        pose = msg.pose.pose
        self.gz_x = pose.position.x
        self.gz_y = pose.position.y
        self.gz_z = pose.position.z
        self.gz_qx = pose.orientation.x
        self.gz_qy = pose.orientation.y
        self.gz_qz = pose.orientation.z
        self.gz_qw = pose.orientation.w
        
    

    def write_row(self):
        if self.latest_twin is None:
            return

        now = self.get_clock().now().nanoseconds / 1e9
        pose = self.latest_twin.pose.pose
        twist = self.latest_twin.twist.twist

        self.writer.writerow([
            now,
            self.latest_cmd.linear.x,
            self.latest_cmd.linear.y,
            self.latest_cmd.linear.z,
            self.latest_cmd.angular.z,

            pose.position.x,
            pose.position.y,
            pose.position.z,
            pose.orientation.x,
            pose.orientation.y,
            pose.orientation.z,
            pose.orientation.w,
            twist.linear.x,
            twist.linear.y,
            twist.linear.z,
            twist.angular.z,

            self.gz_x,
            self.gz_y,
            self.gz_z,
            self.gz_qx,
            self.gz_qy,
            self.gz_qz,
            self.gz_qw,
        ])
        self.csv_file.flush()

    def destroy_node(self):
        try:
            self.csv_file.close()
        except Exception:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = LoggerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
