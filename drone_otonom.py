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

#from std_msgs.msg import Header
def konum(data):
	knm = data.data
	#rospy.loginfo(knm)

def listener():
	#rospy.init_node('drone_otonomV2', anonymous=True)
	rospy.Subscriber('konum', String, konum) 
	#rospy.spin()   
def move():

	deger ="0.0 0.0 0.0 0.0"
	pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget,queue_size=10)

	rospy.init_node('talker',anonymous=True)                           

	msg = PositionTarget()

	msg.header.stamp = rospy.Time.now()
	msg.header.frame_id= "world"
	msg.coordinate_frame = 8
	msg.type_mask=455

	msg.velocity.x = 0.0
	msg.velocity.y = 0.0
	msg.velocity.z = 0.0
	msg.yaw = 0.0
	msg.yaw_rate = 1.0

	def yaz():
		print "girdi"
		global deger
		deger = input()
		deger2 = deger.split(" ")
		print float(deger2[0])
		msg.velocity.x = float(deger2[0])
		msg.velocity.y = float(deger2[1])
		msg.velocity.z = float(deger2[2])

		msg.yaw = float(deger2[3])

		t4 = threading.Thread(target=yaz)
		t4.start()



	t4 = threading.Thread(target=yaz)
	t4.start()

	#rate = rospy.Rate(0.1)                                                                                                   
	while not rospy.is_shutdown():
		

		pub.publish(msg)
		listener()
		

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


