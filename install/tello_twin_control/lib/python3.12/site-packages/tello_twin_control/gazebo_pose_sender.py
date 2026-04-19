import subprocess

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class GazeboPoseSender(Node):
    def __init__(self):
        super().__init__('gazebo_pose_sender')

        self.subscription = self.create_subscription(
            Odometry,
            '/tello_state',
            self.state_callback,
            10
        )

        self.world_name = 'simple_drone_world'
        self.model_name = 'simple_drone'

        self.last_time = self.get_clock().now()
        self.update_interval = 0.1
        self.get_logger().info('gazebo_pose_sender started')

    def state_callback(self, msg: Odometry):
        now = self.get_clock().now()
        dt = (now - self.last_time).nanoseconds / 1e9

        if dt < self.update_interval:
            return

        self.last_time = now

        p = msg.pose.pose.position
        q = msg.pose.pose.orientation

        req = (
            f'name: "{self.model_name}", '
            f'position: {{x: {p.x}, y: {p.y}, z: {p.z}}}, '
            f'orientation: {{x: {q.x}, y: {q.y}, z: {q.z}, w: {q.w}}}'
        )

        cmd = [
            'gz', 'service',
            '-s', f'/world/{self.world_name}/set_pose',
            '--reqtype', 'gz.msgs.Pose',
            '--reptype', 'gz.msgs.Boolean',
            '--timeout', '200',
            '--req', req
        ]

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=3.0
            )

            self.get_logger().info(
                f'Sending pose x={p.x:.2f}, y={p.y:.2f}, z={p.z:.2f}'
            )

            if result.returncode != 0:
                self.get_logger().warning(
                    f'Failed to call Gazebo service: {result.stderr.strip()}'
                )
        except Exception as e:
            self.get_logger().warning(f'Exception while sending pose: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = GazeboPoseSender()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
