#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16

##Computation Libraries
import numpy as np
import math 

pi = math.pi

##Variables
link1_length = 2.5
correction_factor = 0
link_length_1 = 12
link_length_2 = 12

##Compute angles from provided co-ordinates
def compute_angles(x,y,z):

	theta_3 = (math.acos((x**2 + y**2 + (z-link1_length)**2)/((link_length_2**2)+(link_length_1**2)) - 1))

	theta_1 = (math.atan2(y,x))

	theta_2 = math.atan2((z-link1_length),((x**2 + y**2)**0.5))-(theta_3)/2
	
	''' 
	# to reach places where second arm can't reach directly
	if theta_2 < 0:
		theta_2 = 0
		theta_3 = atan2((2-link1_length),abs(x-link_length_1))
	'''
	theta_3 += pi/2	

	theta_1 = math.degrees(theta_1)
	theta_2 = math.degrees(theta_2)
	theta_3 = math.degrees(theta_3)

	return theta_1, theta_2, theta_3

def angle_publisher():
	pub = rospy.Publisher('servo',UInt16, queue_size = 10)
	rospy.init_node('angle_publisher', anonymous=True)
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():

		x = input("1:")
		y = input("2:")
		z = input("3:")

		servo_angle_1,servo_angle_2,servo_angle_3 = compute_angles(x,y,z)

		print(servo_angle_1,servo_angle_2,servo_angle_3)
		
		#Workspace limiting conditions
		
		if servo_angle_1<0 or servo_angle_2<0 or servo_angle_3<0:
			print("invalid angles")
			servo_angle_1,servo_angle_2,servo_angle_3=0,0,0

		pub.publish(servo_angle_1)
		pub.publish(servo_angle_2)
		pub.publish(servo_angle_3)

		rate.sleep()

if __name__ == '__main__':
    try:
        angle_publisher()
    except ValueError:
    	print "Target out of reach"
    except rospy.ROSInterruptException: 
        pass

