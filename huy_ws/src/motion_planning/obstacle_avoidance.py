#! /usr/bin/env python

import rospy

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
pub = None

linear_x = 0
angular_z = 0

def clbk_laser(msg):
    regions = {
        'right':  min(min(msg.ranges[90:125]), 10),
        'fright': min(min(msg.ranges[126:161]), 10),
        'front':  min(min(msg.ranges[162:197]), 10),
        'fleft':  min(min(msg.ranges[198:233]), 10),
        'left':   min(min(msg.ranges[234:270]), 10),
    }
    
    take_action(regions)
    
def take_action(regions):
    msg = Twist()
    global linear_x
    global angular_z
    #linear_x = 0
    #angular_z = 0
    
    state_description = ''
    
    if regions['front'] > 0.5 and regions['fleft'] > 0.5 and regions['fright'] > 0.5:
        state_description = 'case 1 - nothing'
        linear_x = 0.2
        angular_z = 0
    elif regions['front'] < 0.5 and regions['fleft'] > 0.5 and regions['fright'] > 0.5:
        state_description = 'case 2 - front'
        if angular_z < 0:
            linear_x = 0.1
            angular_z = -0.5
        else :
            linear_x = 0.1
            angular_z = 0.5
    elif regions['front'] > 0.5 and regions['fleft'] > 0.5 and regions['fright'] < 0.5:
        state_description = 'case 3 - fright'
        linear_x = 0.1
        angular_z = 0.5
    elif regions['front'] > 0.5 and regions['fleft'] < 0.5 and regions['fright'] > 0.5:
        state_description = 'case 4 - fleft'
        linear_x = 0.1
        angular_z = -0.5
    elif regions['front'] < 0.5 and regions['fleft'] > 0.5 and regions['fright'] < 0.5:
        state_description = 'case 5 - front and fright'
        linear_x = 0.1
        angular_z = 0.5
    elif regions['front'] < 0.5 and regions['fleft'] < 0.5 and regions['fright'] > 0.5:
        state_description = 'case 6 - front and fleft'
        linear_x = 0.1
        angular_z = -0.5
    elif regions['front'] < 0.5 and regions['fleft'] < 0.5 and regions['fright'] < 0.5:
        state_description = 'case 7 - front and fleft and fright'
        if angular_z < 0:
            linear_x = -0.1
            angular_z = -0.5
        else :
            linear_x = -0.1
            angular_z = 0.5
    elif regions['front'] > 0.5 and regions['fleft'] < 0.5 and regions['fright'] < 0.5:
        state_description = 'case 8 - fleft and fright'
        linear_x = 0.2
        angular_z = 0
    else:
        state_description = 'unknown case'
        rospy.loginfo(regions)

    rospy.loginfo(state_description)
    msg.linear.x = linear_x
    msg.angular.z = angular_z
    pub.publish(msg)

def main():
    global pub
    
    rospy.init_node('reading_laser')
    
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
    
    sub = rospy.Subscriber('/scan', LaserScan, clbk_laser)
    
    rospy.spin()

if __name__ == '__main__':
    main()