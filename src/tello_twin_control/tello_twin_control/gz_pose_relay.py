import subprocess
import threading

import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry


class GzPoseRelay(Node):
    def __init__(self):
        super().__init__('gz_pose_relay')

        self.pub = self.create_publisher(Odometry, '/gazebo_state', 10)

        self.process = subprocess.Popen(
            ['gz', 'topic', '-e', '-t', '/world/simple_drone_world/dynamic_pose/info'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        self.thread = threading.Thread(target=self.read_loop, daemon=True)
        self.thread.start()

        self.get_logger().info('gz_pose_relay started')

    def publish_pose(self, px, py, pz, qx, qy, qz, qw):
        msg = Odometry()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'world'
        msg.child_frame_id = 'simple_drone'

        msg.pose.pose.position.x = px
        msg.pose.pose.position.y = py
        msg.pose.pose.position.z = pz
        msg.pose.pose.orientation.x = qx
        msg.pose.pose.orientation.y = qy
        msg.pose.pose.orientation.z = qz
        msg.pose.pose.orientation.w = qw

        self.pub.publish(msg)

    def read_loop(self):
        current_name = None
        in_position = False
        in_orientation = False

        px = py = pz = 0.0
        qx = qy = qz = 0.0
        qw = 1.0

        for raw_line in self.process.stdout:
            line = raw_line.strip()

            if not line:
                continue

            if line == 'pose {':
                current_name = None
                in_position = False
                in_orientation = False
                px = py = pz = 0.0
                qx = qy = qz = 0.0
                qw = 1.0
                continue

            if line == 'position {':
                in_position = True
                in_orientation = False
                continue

            if line == 'orientation {':
                in_position = False
                in_orientation = True
                continue

            if line == '}':
                if current_name == 'simple_drone' and not in_position and not in_orientation:
                    self.publish_pose(px, py, pz, qx, qy, qz, qw)
                in_position = False
                in_orientation = False
                continue

            if ':' not in line:
                continue

            key, value = [x.strip() for x in line.split(':', 1)]

            if key == 'name':
                current_name = value.strip('"')
                continue

            try:
                value = float(value)
            except ValueError:
                continue

            if in_position:
                if key == 'x':
                    px = value
                elif key == 'y':
                    py = value
                elif key == 'z':
                    pz = value
            elif in_orientation:
                if key == 'x':
                    qx = value
                elif key == 'y':
                    qy = value
                elif key == 'z':
                    qz = value
                elif key == 'w':
                    qw = value

    def destroy_node(self):
        try:
            if self.process is not None:
                self.process.terminate()
        except Exception:
            pass
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = GzPoseRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
