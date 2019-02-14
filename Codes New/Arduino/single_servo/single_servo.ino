#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

Servo servo1;

void servo_cb( const std_msgs::UInt16& cmd_msg)
{
  servo1.write(cmd_msg.data); //set servo angle, should be from 0-180  
}

ros::Subscriber<std_msgs::UInt16> sub("servo", servo_cb);

void setup()
{ 
  nh.initNode();
  nh.subscribe(sub);
  
  servo1.attach(13); //attach it to pin D5
}

void loop()
{
  nh.spinOnce();  //to execute callback function
  delay(1);
}
