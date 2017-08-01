#!/usr/bin/env python
#-*- coding:utf-8 -*-

#注意#
"""
inspection中に緊急停止ボタン押されるので、
確実に、smach_stateはfaildします(出口には行く前に止められるから。)
"""

#this URL "https://git.hsr.io/erasers2017/common.git"
from common import smach_states as css
import smach
import smach_ros
import threading
import rospy
from tmc_msgs.msg import Voice
#レフェリーの指示のサブスク用_ポケスフィになるなら廃止してよい。
from std_msgs.msg import String

print "loading hsrb_interface"
import hsrb_interface
#---------initialize_hsr_system-----
robot = hsrb_interface.Robot()
omni_base = robot.get('omni_base')
#---------setting_talk_request------
global talk_pub, talk_data
talk_pub = rospy.Publisher("/talk_request", Voice, queue_size=10)
talk_data = Voice()
talk_data.language = 1
"""
0:japanese
1:english
"""
#-----------------------------------
print "complete setup!"

#MP(map_point)の設定#
MP = {"point":[1.0,0.0,0.0],
      "exit":[2.0,0.0,0.0]}

class Move(smach.State):
      def __init__(self,timeout=30.):
          smach.State.__init__(self, outcomes=["success","timeout"])
      def execute(self,userdata):
          try:
            global talk_pub, talk_data, MP
            talk_data.sentence = "start inspection, go to waypoint"
            talk_pub.publish(talk_data)
            rospy.sleep(3.0)#後日デバックしまする。
            omni_base.go(MP["point"][0],MP["point"][1],MP["point"][1])
            return "success"
          except:
            talk_data.sentence = "I faild inspection because I faild moving. Sorry."
            talk_pub.publish(data)
            return "timeout"

class Waitalk(smach.State):
      def __init__(self,timeout=120.):
          smach.State.__init__(self, outcomes=["success","timeout"])
          self.mutex = threading.Lock()
          self.pass_call = False
          self.rospy.Subscriber("/ref_talk",String,self.cb,queue_size=1)
      def cb(self,data):
          self.mutex.acquire()
          if data.data == "ok":
             self.pass_call = True
          self.mutex.release()
      def execute(self,userdata):
          talk_data.sentence = "I stay waipoint"
          talk_pub.publish(talk_data)
          try:
            self.mutex.acquire()
            if self.pass_call:
               return "success"
          except:
            return "timeout"
          
class Goexit(smach.State):
      def __init__(self):
          smach.State.__init__(self, outcomes=["success","timeout"])
      def execute(self,userdata):
          global talk_pub, MP
　　　　　　　　　　talk_data.sentence = "I wanna go exit. please push emergency button."
          talk_pub.publish(talk_data)
          rospy.sleep(3.0)#同じく実際に動かすのでまってちょwww

          try:
            omni_base.go(MP["exit"][0],MP["exit"][1],MP["exit"][2])
            return "success"
          except:
            return "timeout"

def main():
    sm = smach.StateMachine(outcomes=['complete', 'faild'])

    with sm:

         smach.StateMachine.add("w_door", css.WaitDoorOpen(),
                                transitions={"success":"wayp1",
                                             "timeout":"faild",
                                             "failure":"faild"})

         smach.StateMachine.add("wayp1", Move(),
                                transitions={"success":"waitalk",
                                             "timeout":"faild"})

         smach.StateMachine.add("waitalk", Waitalk(),
                                transitions={"success":"w_hand",
                                             "timeout":"faild"})

         smach.StateMachine.add("w_hand", css.WaitHandPushed(),
                                transitions={"success":"exit",
                                             "timeout":"faild",
                                             "failure":"faild"})

         smach.StateMachine.add("exit", Goexit(),
                                transitions={"success":"complete",
                                             "timeout":"faild"})


# Create and start the introspection server
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    outcome = sm.execute()
    rospy.spin()


if __name__ == "__main__":
    print "loading complete"
    main()
