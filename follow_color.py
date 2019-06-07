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
from mavros_msgs.msg import State

msg = PositionTarget()

lastErrorY = 0
lastErrorR = 0

current_state=State()

def call_back(data):
	rospy.loginfo("cameradan veri geldi")
	global lastErrorY
	global lastErrorR

	XY = data.data
	XY = XY.split(" ")

	x = float(XY[0])
	y = float(XY[1])
	r = float(XY[2])

	# -----------------------
	errorY = 165-y

	kp = 1.0/100.0
	kd = 1.0/150.0

	turevY = errorY-lastErrorY
	yukselmeY =  errorY*kp + turevY*kd
	msg.velocity.z = yukselmeY
	
	lastErrorY = errorY

	# -----------------------

	errorR = 55 - r

	kpR = 1.0/80.0
	kdR = 1.0/100.0

	turevR = errorR-lastErrorR
	yaklasma =  errorR*kpR + turevR*kdR
	msg.velocity.y = yaklasma
	
	lastErrorR = errorR

	# -----------------------


	errorX = 300-x
	
	if errorX < 30 and errorX > -30:
		errorX =0


	yaw_target = yaw_degrees + (errorX*35)/300

	if yaw_target >= 360:
		yaw_target = yaw_target - 360

	if yaw_target < 0:
		yaw_target = yaw_target + 360	
	print "r = ", r, " errorX = ", errorX , " yaw_degrees " , yaw_degrees, " yaw_target", yaw_target
	
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
    #print "yaw_degrees HAS " , yaw_degrees
	

def state_cb(state):
    global current_state
    current_state = state

if  __name__ == '__main__':

	global current_state

	rospy.init_node('talker',anonymous=True)
	rate = rospy.Rate(20)
	mavros.set_namespace('mavros')
	rospy.wait_for_service('/mavros/cmd/arming')
	 	
	try:
		armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
		armService(True)
	except rospy.ServiceException, e:
	 	pass
	
	set_mode = rospy.ServiceProxy(mavros.get_topic('set_mode'), mavros_msgs.srv.SetMode)
	state_sub = rospy.Subscriber(mavros.get_topic('state'), State, state_cb)

	rospy.loginfo("arming succesfull")

	pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget,queue_size=10)

	msg.header.stamp = rospy.Time.now()
	msg.header.frame_id = "world"
	msg.coordinate_frame = PositionTarget.FRAME_BODY_OFFSET_NED
	msg.type_mask = PositionTarget.IGNORE_VX | PositionTarget.IGNORE_VY | PositionTarget.IGNORE_VZ | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ | PositionTarget.IGNORE_YAW| PositionTarget.IGNORE_YAW_RATE

	msg.position.x = 0.0
	msg.position.y = 0.0
	msg.position.z = 2.0
	#msg.yaw = 0.0

	counter = 0

	rospy.loginfo("ilk veri gonderilcek")


	while current_state.mode != "OFFBOARD":
			
		pub.publish(msg)
		 
		set_mode(0,'OFFBOARD')
		rospy.loginfo("OFFBOARD mod istegi gonderildi")
		
		rate.sleep()


	msg.type_mask = PositionTarget.IGNORE_PX | PositionTarget.IGNORE_PY | PositionTarget.IGNORE_PZ | PositionTarget.IGNORE_AFX | PositionTarget.IGNORE_AFY | PositionTarget.IGNORE_AFZ | PositionTarget.IGNORE_YAW_RATE

	msg.velocity.x = 0.0
	msg.velocity.y = 0.0
	msg.velocity.z = 0.0
	msg.yaw = 0.0
	rospy.loginfo("velocity asamasina gecildi")
	try:
		
		sub = rospy.Subscriber ('/mavros/local_position/odom', Odometry, get_rotation)	
	
		rospy.Subscriber('konum', String, call_back) # kamera goruntusunden x,y kordinatlari
		
		rospy.loginfo("Subscriber islemleri tamam")
		

		while not rospy.is_shutdown():
			
			pub.publish(msg)

			rate.sleep()

			
		
		
		

	except rospy.ROSInterruptException:
		pass


