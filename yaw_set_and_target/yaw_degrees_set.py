#!/usr/bin/env python

import rospy 
from std_msgs.msg import String 


if __name__ == '__main__':
	pub = rospy.Publisher('yaw_degrees', String, queue_size=10)
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(10)

	while (True):
		yaw_ = input()
		#convert to degrees
		yaw_ = (float(yaw_)*6.3)/360.0
	
		pub.publish(str(yaw_))  
		rate.sleep() 