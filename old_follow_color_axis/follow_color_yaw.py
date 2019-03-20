#!/usr/bin/env python

import rospy 
import mavros
#from threading import Thread, Timer
#import time
import threading
import time
import math
#from geometry_msgs.msg import Twist
from mavros_msgs.msg import PositionTarget
from mavros_msgs.srv import *
from std_msgs.msg import String
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion, quaternion_from_euler

msg = PositionTarget()
#from std_msgs.msg import Header
#

def call_back(data):
	#global msg
	
	#global yaw_degrees

	
	XY = data.data
	XY = XY.split(" ")

	x= float(XY[0])
	y= float(XY[1])
	errorX = 300-x
	
	if errorX < 30 and errorX > -30:
		errorX =0


	yaw_target = yaw_degrees + (errorX*35)/300

	if yaw_target >= 360:
		yaw_target = yaw_target - 360

	if yaw_target < 0:
		yaw_target = yaw_target + 360	
	print "errorX = ", errorX , "yaw_degrees " , yaw_degrees, "yaw_target", yaw_target
	
	msg.yaw = float(yaw_target*math.pi/180.0)

yaw_degrees = roll = pitch = yaw = 0.0

def get_rotation (msg):
    global yaw_degrees,roll, pitch, yaw
#    print msg.pose.pose.orientation
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x, orientation_q.y, orientation_q.z, orientation_q.w]
    (roll, pitch, yaw) = euler_from_quaternion (orientation_list)
    yaw_degrees = yaw * 180.0 / math.pi
    if( yaw_degrees < 0 ):
        yaw_degrees += 360.0
    print "yaw_degrees HAS " , yaw_degrees
	



if  __name__ == '__main__':

	rospy.init_node('talker',anonymous=True)
	rate = rospy.Rate(20)

	rospy.wait_for_service('/mavros/cmd/arming')
	 	
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(True)
	except rospy.ServiceException, e:
	 	pass
	
	print "harun"
	try:
		
		sub = rospy.Subscriber ('/mavros/local_position/odom', Odometry, get_rotation)	
	
		rospy.Subscriber('konum', String, call_back) # kamera goruntusunden x,y kordinatlari
		pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget,queue_size=10)
		
		print "mdmmd"

		
		print "girdimv"
		
		msg.header.stamp = rospy.Time.now()
		msg.header.frame_id = "world"
		msg.coordinate_frame = PositionTarget.FRAME_BODY_NED
		msg.type_mask = PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ | PositionTarget.IGNORE_YAW_RATE

		msg.position.x = 0.0
		msg.position.y = 0.0
		msg.position.z = 2.0
		msg.yaw = 0.0


		while not rospy.is_shutdown():
			
			pub.publish(msg)
			rate.sleep()

			
		
		
		

	except rospy.ROSInterruptException:
		pass


