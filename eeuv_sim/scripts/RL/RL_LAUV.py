#!/usr/bin/python3

"""
Node to control U-CAT in Gazebo using keyboard input
@author: You
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32MultiArray
import sys
import termios
import tty

class SendActionROS2(Node):
    def __init__(self):
        super().__init__('keyboard_control')
        self.wing_pub = self.create_publisher(Float32MultiArray, '/ucat/wing_angle_cmd', 10)
        self.thrust_pub = self.create_publisher(Float32MultiArray, '/ucat/thruster_cmd', 10)
        
        self.wings_cmd = Float32MultiArray()
        self.wings_cmd.data = [0.0, 0.0, 0.0, 0.0]
        self.thruster_cmd = Float32MultiArray()
        self.thruster_cmd.data = [0.0]

    def publish_command(self, wings, thruster):
        self.wings_cmd.data = wings
        self.thruster_cmd.data = [thruster]
        self.wing_pub.publish(self.wings_cmd)
        self.thrust_pub.publish(self.thruster_cmd)


def get_key():
    """Read a single keypress from stdin"""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def main(args=None):
    rclpy.init(args=args)
    node = SendActionROS2()

    print("Use keys to control U-CAT:")
    print("w/s: forward/back thruster")
    print("a/d: roll fins left/right")
    print("q/e: pitch fins up/down")
    print("z/x: yaw fins left/right")
    print("space: stop thruster")
    print("CTRL-C to quit")

    wings = [0.0, 0.0, 0.0, 0.0]
    thruster = 0.0
    step = 5.0  # degree per keypress
    thrust_step = 1.0  # N per keypress

    try:
        while rclpy.ok():
            key = get_key()
            if key == '\x03':  # CTRL-C
                break
            elif key == 'w':
                thruster += thrust_step
            elif key == 's':
                thruster -= thrust_step
            elif key == ' ':
                thruster = 0.0
            elif key == 'a':
                wings[0] += step  # adjust fins as you like
            elif key == 'd':
                wings[0] -= step
            elif key == 'q':
                wings[1] += step
            elif key == 'e':
                wings[1] -= step
            elif key == 'z':
                wings[2] += step
            elif key == 'x':
                wings[2] -= step

            node.publish_command(wings, thruster)
            print(f"Wings: {wings}, Thruster: {thruster}")

    except KeyboardInterrupt:
        pass

    print("Stopping U-CAT...")
    node.publish_command([0.0, 0.0, 0.0, 0.0], 0.0)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
