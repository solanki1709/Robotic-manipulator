#!/usr/bin/env python

import rospy
from std_msgs.msg import UInt16

def angle_publisher():

	pub = rospy.Publisher('servo',UInt16, queue_size = 10)
	rospy.init_node('angle_publisher', anonymous=True)
	rate = rospy.Rate(10)
	while not rospy.is_shutdown():
		a = input("1:")
		pub.publish(a)
		rate.sleep()

if __name__ == '__main__':
	try:
		angle_publisher()
	except rospy.ROSInterruptException: 
		pass
