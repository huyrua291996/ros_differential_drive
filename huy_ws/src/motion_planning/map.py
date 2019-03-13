#! /usr/bin/env python

import rospy

from nav_msgs.msg import *
from std_msgs.msg import *

def clbk_map(msg):
    # 720 / 5 = 144
    rospy.loginfo(len(list(msg.data)))

def main():
    rospy.init_node('reading_map')
    mymap = OccupancyGrid()
    sub = rospy.Subscriber('/map', OccupancyGrid, clbk_map)
    
    rospy.spin()

if __name__ == '__main__':
    main()