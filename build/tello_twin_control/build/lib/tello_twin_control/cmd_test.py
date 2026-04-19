import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdTestNode(Node):
    def __init__(self):
        super().__init__('cmd_test')
        self.publisher_ = self.create_publisher(Twist, '/tello_cmd', 10)
        self.timer = self.create_timer(0.1, self.publish_cmd)
        self.start_time = self.get_clock().now().nanoseconds / 1e9

    def publish_cmd(self):
        now = self.get_clock().now().nanoseconds / 1e9
        t = now - self.start_time

        msg = Twist()

        if t < 2.0:
            pass
        elif t < 6.0:
            msg.linear.x = 1.0
        elif t < 8.0:
            pass
        elif t < 12.0:
            msg.angular.z = 1.0
        else:
            self.start_time = now

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'cmd: fb={msg.linear.x:.2f}, lr={msg.linear.y:.2f}, '
            f'ud={msg.linear.z:.2f}, yaw={msg.angular.z:.2f}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = CmdTestNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
