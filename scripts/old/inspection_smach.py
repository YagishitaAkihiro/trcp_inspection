#!/usr/bin/env python
#-*- coding:utf-8 -*-

import hsrb_interface
from common import smach_states as css
import smach
import smach_ros
import rospy
#import actlib_base as base
from tmc_msgs.msg import Voice
from std_msgs.msg import String
import sys
from geometry_msgs.msg import WrenchStamped

robot = hsrb_interface.Robot()
omni_base = robot.get('omni_base')

#rospy.init_node("ins")
print "aaaa"

#base=base.actlib()
global talk_pub, talk_data
talk_pub = rospy.Publisher("/talk_request", Voice, queue_size=10)
talk_data = Voice()
talk_data.language = 1

class Move(smach.State):
      def __init__(self):
          smach.State.__init__(self, outcomes=["success","timeout"])
      def execute(self,userdata):
          try:
            global talk_pub, talk_data
            talk_data.sentence = "start"
            talk_pub.publish(talk_data)
            omni_base.go(5.05,1.69,0.0)
            return "success"
          except:
            talk_data.sentence = "I faild inspection"
            talk_pub.publish(data)
            return "timeout"

class Waitalk(smach.State):
      def __init__(self,timeout=120.):
          smach.State.__init__(self, outcomes=["success","timeout"])
      def execute(self,userdata):
         # self.pass_call = "No"
          try:
            talk_data.sentence = "I stay waipoint"
            talk_pub.publish(talk_data)
            return "success"
          except:
            return "timeout"
          
class Goexit(smach.State):
      def __init__(self):
          smach.State.__init__(self, outcomes=["success","timeout"])
      def execute(self,userdata):
          global talk_pub
          rospy.sleep(1.5)
          try:
            omni_base.go(13.3,-0.23,-0.79)#exitのところ。
            rospy.sleep(5.0)
            talk_data.sentence = "I wanna go exit. please push emergency button."
            talk_pub.publish(talk_data)
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
"""単体クラステスト？まだ導入してない
    if len(sys.argv) < 2:
        print 'Usage: rosrun common smach_states.py <class_name> args...'
        quit()
    exp = [sys.argv[1], '(']
    exp.append(','.join(sys.argv[2:]))
    exp.append(')')
    exp = ''.join(exp)
    print 'state: '+exp

    state = eval(exp)
    outcomes = state.get_registered_outcomes()
    sm = smach.StateMachine(outcomes=outcomes)
    with sm:
        smach.StateMachine.add('TEST', state, transitions={k:k for k in outcomes})
    sm.userdata.params = {}
    print 'outcome: '+sm.execute()
    print 'params: '+str(sm.userdata.params)
"""
