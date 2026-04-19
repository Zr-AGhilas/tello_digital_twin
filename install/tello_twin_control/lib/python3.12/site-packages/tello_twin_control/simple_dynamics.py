import math

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion


def yaw_to_quaternion(yaw: float) -> Quaternion:
    q = Quaternion()
    q.w = math.cos(yaw / 2.0)
    q.x = 0.0
    q.y = 0.0
    q.z = math.sin(yaw / 2.0)
    return q


class SimpleDynamicsNode(Node):
    def __init__(self):
        super().__init__('simple_dynamics')

        self.cmd_sub = self.create_subscription(
            Twist, '/tello_cmd', self.cmd_callback, 10
        )
        self.odom_pub = self.create_publisher(Odometry, '/tello_state', 10)

        self.timer_dt = 0.02
        self.timer = self.create_timer(self.timer_dt, self.update_dynamics)

        # commanded velocities
        self.vx_cmd = 0.0
        self.vy_cmd = 0.0
        self.vz_cmd = 0.0
        self.r_cmd = 0.0

        # actual velocities
        self.vx = 0.0
        self.vy = 0.0
        self.vz = 0.0
        self.r = 0.0

        # state
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.yaw = 0.0

        # gains
        self.kx = 1.0
        self.ky = 1.0
        self.kz = 1.0
        self.kr = 1.0

        # first-order time constants
        self.tau_x = 0.6
        self.tau_y = 0.6
        self.tau_z = 0.6
        self.tau_r = 0.4

    def cmd_callback(self, msg: Twist):
        self.vx_cmd = self.kx * msg.linear.x
        self.vy_cmd = self.ky * msg.linear.y
        self.vz_cmd = self.kz * msg.linear.z
        self.r_cmd = self.kr * msg.angular.z

    def update_dynamics(self):
        dt = self.timer_dt

        # first-order velocity dynamics
        self.vx += ((self.vx_cmd - self.vx) / self.tau_x) * dt
        self.vy += ((self.vy_cmd - self.vy) / self.tau_y) * dt
        self.vz += ((self.vz_cmd - self.vz) / self.tau_z) * dt
        self.r += ((self.r_cmd - self.r) / self.tau_r) * dt

        # integrate yaw
        self.yaw += self.r * dt

        # body-frame velocity -> world-frame position
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)

        vx_world = cos_yaw * self.vx - sin_yaw * self.vy
        vy_world = sin_yaw * self.vx + cos_yaw * self.vy

        self.x += vx_world * dt
        self.y += vy_world * dt
        self.z += self.vz * dt

        # publish odometry
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.child_frame_id = 'base_link'

        msg.pose.pose.position.x = self.x
        msg.pose.pose.position.y = self.y
        msg.pose.pose.position.z = self.z
        msg.pose.pose.orientation = yaw_to_quaternion(self.yaw)

        msg.twist.twist.linear.x = self.vx
        msg.twist.twist.linear.y = self.vy
        msg.twist.twist.linear.z = self.vz
        msg.twist.twist.angular.z = self.r

        self.odom_pub.publish(msg)

        self.get_logger().info(
            f'state: x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f}, '
            f'yaw={self.yaw:.2f}, vx={self.vx:.2f}, vy={self.vy:.2f}, '
            f'vz={self.vz:.2f}, r={self.r:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = SimpleDynamicsNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
