#!/usr/bin/env python
# vim:set ts=4 sw=4 et:
#
# Copyright 2015 UAVenture AG.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
# Updated: Tarek Taha : tarek.taha@kustar.ac.ae, Vladimir Ermakov
#    - Changed topic names after re-factoring : https://github.com/mavlink/mavros/issues/233
#    - Use mavros.setpoint module for topics

import rospy
import thread
import threading
import time
import mavros

from math import *
from mavros.utils import *
#from mavros import setpoint as SP
#from tf.transformations import quaternion_from_euler
from mavros_msgs.msg import PositionTarget
from mavros_msgs.srv import *
from std_msgs.msg import String
from mavros_msgs.srv import CommandBool, SetMode

class SetpointPosition:
    """
    This class sends position targets to FCU's position controller
    """
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.yaw= 0.0
        # publisher for mavros/setpoint_position/local
        self.pub = rospy.Publisher('/mavros/setpoint_raw/local', PositionTarget,queue_size=10)
        #self.pub = SP.get_pub_position_local(queue_size=10)
        # subscriber for mavros/local_position/local
        #self.sub = rospy.Subscriber('yaw_degrees', String, self.reached)
        #self.sub = rospy.Subscriber(mavros.get_topic('local_position', 'pose'),
        #                            SP.PoseStamped, self.reached)

        try:
            thread.start_new_thread(self.navigate, ())
        except:
            fault("Error: Unable to start thread")

        # TODO(simon): Clean this up.
        self.done = False
        self.done_evt = threading.Event()
    """
    def reached(self,data):
        
        yaw_ =data.data

        if yaw_ > self.yaw -10 and yaw_ < self.yaw +10: 
            self.done = True
            #self.done_evt.set()
"""

    def navigate(self):
        rate = rospy.Rate(10)   # 10hz

        msg = PositionTarget()
        msg.header.stamp = rospy.Time.now()
        msg.header.frame_id= "world"
        msg.coordinate_frame = 8
        msg.type_mask=2503
        """
        msg = SP.PoseStamped(
            header=SP.Header(
                frame_id="base_footprint",  # no matter, plugin don't use TF
                stamp=rospy.Time.now()),    # stamp should update
        )"""

        while not rospy.is_shutdown():
            msg.velocity.x = self.x
            msg.velocity.y = self.y
            msg.velocity.z = self.z
            msg.yaw = self.yaw
            # For demo purposes we will lock yaw/heading to north.
            
            self.pub.publish(msg)
            rate.sleep()

    def set(self, x, y, z,yaw, delay=0, wait=True):
        self.done = False
        self.x = x
        self.y = y
        self.z = z
        self.yaw = (yaw*6.3)/360

        """     
        if wait:
            rate = rospy.Rate(5)
            while not self.done and not rospy.is_shutdown():
                rate.sleep()
        """
        time.sleep(delay)

    

def setpoint_demo():
    rospy.init_node('talker',anonymous=True)
    #mavros.set_namespace()  # initialize mavros module with default namespace
    rate = rospy.Rate(10)

    setpoint = SetpointPosition()
    
    #setOffboardMode
    set_mode_client = rospy.ServiceProxy('/mavros/set_mode', SetMode) 
    set_mode_client(base_mode=0, custom_mode="OFFBOARD")
   
    rospy.loginfo("Climb")
    setpoint.set(0.0, 0.0, 2.0, 0.0, 3.0)
    

    rospy.loginfo("yaw")
    setpoint.set(0.0, 0.0, 0.0, -90.0,6.0)
    
    rospy.loginfo("Fly to the forward")
    setpoint.set(0.0, 2.0, 0.0, -90.0,3)

    rospy.loginfo("yaw 180")
    setpoint.set(0.0, 0.0, 0.0, 90.0,6.0)

    rospy.loginfo("Fly to the forward")
    setpoint.set(0.0, 2.0, 0.0, 90.0,3.0)


   

if __name__ == '__main__':


   

    rospy.wait_for_service('/mavros/cmd/arming')
         
    try:
        armService = rospy.ServiceProxy('/mavros/cmd/arming', mavros_msgs.srv.CommandBool)
        armService(True)



    except rospy.ServiceException, e:
        pass

    print "started"
    try:
        setpoint_demo()
    except rospy.ROSInterruptException:
        pass
