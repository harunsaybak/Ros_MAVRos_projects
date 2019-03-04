#!/usr/bin/env python

import rospy 
#from threading import Thread, Timer
#import time
import threading
import time
#from geometry_msgs.msg import Twist
from geometry_msgs.msg import TwistStamped
from mavros_msgs.srv import *
#from std_msgs.msg import Header

def move():

	deger ="0 0 0"
	pub = rospy.Publisher('/mavros/setpoint_velocity/cmd_vel', TwistStamped,queue_size=10)
       
	rospy.init_node('talker',anonymous=True)                           

	twist = TwistStamped()
	twist.header.stamp = rospy.Time()
	
	twist.twist.linear.z = 0.0
	twist.twist.linear.x = 0.0
	twist.twist.linear.y = 0.0
	
	twist.twist.angular.x = 0.0
	twist.twist.angular.y = 0.0
	twist.twist.angular.z = 0.0

	def yaz():
	    global deger
	    deger = input()
	    deger2 = deger.split(" ")
	    twist.twist.linear.x = float(deger2[0])
	    twist.twist.linear.y = float(deger2[1])
	    twist.twist.linear.z = float(deger2[2])
	    
	    t4 = threading.Thread(target=yaz)
	    t4.start()



	t4 = threading.Thread(target=yaz)
	t4.start()

	#rate = rospy.Rate(0.1)                                                                                                   
	while not rospy.is_shutdown():
		

		pub.publish(twist)
		

		#rate.sleep()                                                                            
		

if  __name__ == '__main__':
	
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(True)
	except rospy.ServiceException, e:
		pass

	print "harun"
	try:
		move()
	except rospy.ROSInterruptException:
		pass


