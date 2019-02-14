#!/usr/bin/env python

import rospy

from std_msgs.msg import UInt16


##Computation Libraries
import numpy as np
import math 

##Variables
initial_link_length = 2.5
correction_factor = 0
link_length = 12

def compute_co_ordinates(theta_1,theta_2,theta_3):
	theta_2*=-1
	theta_3*=-1 
	theta_1 = math.radians(theta_1)
	theta_2 = math.radians(theta_2)

	#Servo shifted by 90 degrees
	theta_3 = math.radians(theta_3) + math.pi/2 
	

	#Creation and multiplication of transformation matrices
	transformation_matrix_0_to_1 = np.matrix([[math.cos(theta_1),0,-math.sin(theta_1),0],[math.sin(theta_1),0,math.cos(theta_1),0],[0,-1,0,initial_link_length],[0,0,0,1]])

	transformation_matrix_1_to_2 = np.matrix([[math.cos(theta_2),-math.sin(theta_2),0,link_length*math.cos(theta_2)],[math.sin(theta_2),math.cos(theta_2),0,link_length*math.sin(theta_2)],[0,0,1,0],[0,0,0,1]])
	
	transformation_matrix_2_to_3 = np.matrix([[math.cos(theta_3),-math.sin(theta_3),0,link_length*math.cos(theta_3)],[math.sin(theta_3),math.cos(theta_3),0,link_length*math.sin(theta_3)],[0,0,1,correction_factor],[0,0,0,1]])	
	
	transformation_matrix_0_to_3 = transformation_matrix_0_to_1*transformation_matrix_1_to_2*transformation_matrix_2_to_3

	return transformation_matrix_0_to_3

def angle_publisher():
	pub = rospy.Publisher('servo',UInt16, queue_size = 10)
	rospy.init_node('angle_publisher', anonymous=True)
	rate = rospy.Rate(10)

	while not rospy.is_shutdown():
		servo_angle_1 = input("1:")

		servo_angle_2 = input("2:")

		servo_angle_3 = input("3:")

		transformationMatrix = compute_co_ordinates(servo_angle_1,servo_angle_2,servo_angle_3)

		(x,y,z) = (transformationMatrix[0,3],transformationMatrix[1,3],transformationMatrix[2,3]) 

		print(x,y,z)

		if(servo_angle_1<0 or servo_angle_2<0 or servo_angle_3<0) or (servo_angle_1>180 or servo_angle_2>180 or servo_angle_3>180):
			print("invalid angles")
			servo_angle_1,servo_angle_2,servo_angle_3 = 0,0,0

		pub.publish(servo_angle_1)
		pub.publish(servo_angle_2)
		pub.publish(servo_angle_3)

		rate.sleep()

if __name__ == '__main__':
    try:
        angle_publisher()
    except rospy.ROSInterruptException: 
        pass

