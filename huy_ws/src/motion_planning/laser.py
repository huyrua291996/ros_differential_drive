#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan

def clbk_laser(msg):
    # 720 / 5 = 144
    regions = [
        min(min(msg.ranges[90:125]), 10),
        min(min(msg.ranges[126:161]), 10),
        min(min(msg.ranges[162:197]), 10),
        min(min(msg.ranges[198:233]), 10),
        min(min(msg.ranges[234:270]), 10),
    ]
    rospy.loginfo(regions)

def main():
    rospy.init_node('reading_laser')
    
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    main()