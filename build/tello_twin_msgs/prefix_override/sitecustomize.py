import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/aghilas/tello_twin_ws/install/tello_twin_msgs'
