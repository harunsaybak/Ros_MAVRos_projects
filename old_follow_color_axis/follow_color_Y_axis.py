#!/usr/bin/env python

import rospy 
#from threading import Thread, Timer
#import time
import threading
import time
#from geometry_msgs.msg import Twist
from mavros_msgs.msg import PositionTarget
from mavros_msgs.srv import *
from std_msgs.msg import String

msg = PositionTarget()
#from std_msgs.msg import Header
#
lastErrorY = 0
def call_back(data):
	global msg
	global lastErrorY

	XY = data.data
	XY = XY.split(" ")

	x= float(XY[0])
	y= float(XY[1])

	errorY = 165-y

	kp = 1.0/50.0
	kd = 1.0/75.0

	turevY = errorY-lastErrorY
	yukselmeY =  errorY*kp + turevY*kd
	msg.velocity.z = yukselmeY

	print yukselmeY
	
	lastErrorY = errorY



if  __name__ == '__main__':

	
		
	#rospy.wait_for_service('/mavros/cmd/arming')
	""" 	
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(True)
	except rospy.ServiceException, e:
	 	pass
	"""

	print "harun"
	try:
		rospy.init_node('talker',anonymous=True)
		
		print "mdmmd"

		global msg
		print "girdimv"
		pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget,queue_size=10)
		rospy.Subscriber('konum', String, call_back) # kamera goruntusunden x,y kordinatlari

		msg.header.stamp = rospy.Time.now()
		msg.header.frame_id= "world"
		msg.coordinate_frame = 8
		msg.type_mask=2503

		msg.velocity.x = 0.0
		msg.velocity.y = 0.0
		msg.velocity.z = 0.0
		msg.yaw = 0.0


		while not rospy.is_shutdown():

			pub.publish(msg)

			
		
		
		

	except rospy.ROSInterruptException:
		pass


