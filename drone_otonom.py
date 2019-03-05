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
errorX = 0
lastErrorX = 0;

errorY = 0
lastErrorY = 0;
msg = PositionTarget()
#from std_msgs.msg import Header
def konum(data):
	#print "girdi"
	global errorX
	global errorY
	global lastErrorX
	global lastErrorY

	knm = data.data
	knm = knm.split(" ")
	#print knm[0]
	x= float(knm[0])
	y= float(knm[1])
	#print x
	errorX = 300 - x
	errorY = 225 - y

	kp = 1.0/200.0
	kd = 1.0/300.0

	turevX = errorX-lastErrorX
	donmeX =  errorX*kp + turevX*kd
	lastErrorX = errorX
	#msg.yaw = msg.yaw + donmeX

	turev_yukseklik = errorY-lastErrorY
	yukseklikY =  errorY*kp + turev_yukseklik*kd

	msg.velocity.z = yukseklikY

	#rospy.loginfo(knm)

def listener():
	#rospy.init_node('drone_otonomV2', anonymous=True)
	rospy.Subscriber('konum', String, konum) 
	#rospy.spin()   
def move():
	global msg
	deger ="0.0 0.0 0.0 0.0"
	pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget,queue_size=10)

	rospy.init_node('talker',anonymous=True)                           

	

	msg.header.stamp = rospy.Time.now()
	msg.header.frame_id= "world"
	msg.coordinate_frame = 8
	msg.type_mask=2503

	msg.velocity.x = 0.0
	msg.velocity.y = 0.0
	msg.velocity.z = 0.0
	msg.yaw = 0.0
	#msg.yaw_rate = 0.0
	#pub.publish(msg)
	#time.sleep(3.0)

	def yaz():
		#print "girdi ", errorX
		global msg

		print " z = " , msg.velocity.z

		msg.velocity.x = 0
		msg.velocity.y = 0
		msg.yaw = 0.0

		

		t4 = threading.Thread(target=yaz)
		t4.start()



	t4 = threading.Thread(target=yaz)
	t4.start()

	#rate = rospy.Rate(0.1)                                                                                                   
	while not rospy.is_shutdown():
		
		global msg
		pub.publish(msg)
		listener()
		

		#rate.sleep()                                                                            
		

if  __name__ == '__main__':

	
		
	#rospy.wait_for_service('/mavros/cmd/arming')
	 	
	#try:
	#	#armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
	#	armService(True)
	#except rospy.ServiceException, e:
	# 	pass

	print "harun"
	try:
		
		move()

	except rospy.ROSInterruptException:
		pass


