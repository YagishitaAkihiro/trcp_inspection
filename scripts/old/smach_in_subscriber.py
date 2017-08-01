#!/usr/bin/env python
import roslib; roslib.load_manifest('smach_example')
import rospy
import smach
import smach_ros
from std_msgs.msg import Int16
import time
import threading

class WaitForTwo(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['success', 'in_progress', 'failed'])

        self.mutex = threading.Lock()
        self.two_received = False

        self.subscriber = rospy.Subscriber('/test', Int16, self.callback)

    def callback(self, data):
        self.mutex.acquire()
        if data.data == 2:
            self.two_received = True
        self.mutex.release()

    def execute(self):
        #wait for a maximum of 30 seconds 
        for i in range(0, 300):
            self.mutex.acquire()
            if self.two_received:
                #ok we received 2
                return 'success'

            self.mutex.release()

            time.sleep(.1)
            #still waiting
            return 'in_progress'
        #we didn't get 2 in the 30 sec
        return 'failed'
