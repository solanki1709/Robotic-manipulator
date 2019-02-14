#include <Servo.h> 
#include <ros.h>
#include <std_msgs/UInt16.h>

ros::NodeHandle  nh;

Servo servo1;
Servo servo2;
Servo servo3;
int flag = 0;   //to toggle servos

void servo_cb( const std_msgs::UInt16& cmd_msg)
{
  if(flag == 0)
  {
    servo1.write(cmd_msg.data); //set servo1 angle, should be from 0-180  
    flag = 1;
  }
  else if (flag == 1)
  {
    servo2.write(cmd_msg.data); //set servo2 angle, should be from 0-180
    flag = 2;
  }
  else
  {
    servo3.write(cmd_msg.data); //set servo3 angle, should be from 0-180
    flag = 0;
  }
}

ros::Subscriber<std_msgs::UInt16> sub("servo", servo_cb);

void setup()
{ 
  nh.initNode();
  nh.subscribe(sub);
  
  servo1.attach(13);
  servo2.attach(15);
  servo3.attach(14);

  servo1.write(0);  //set 0 as initial position 
  servo2.write(0);
  servo3.write(0);
}

void loop()
{
  nh.spinOnce();  //to execute callback function
  delay(1);
}

