#!/usr/bin/env python
import roslib
import rospy
import actionlib
import control_msgs.msg
import controller_manager_msgs.srv
import trajectory_msgs.msg

from geometry_msgs.msg import PoseStamped
from move_base_msgs.msg import MoveBaseAction
from move_base_msgs.msg import MoveBaseGoal

import math
import tf

from hsrb_interface import geometry
#from . import robot

action_wait_timeout = 30


def _validate_timeout(timeout):
    """Validate a given timeout value is meaning time value."""
    if timeout < 0.0 or math.isnan(timeout) or math.isinf(timeout):
        raise ValueError("Invalid timeout: {0}".format(timeout))


class actlib():
    global action_client
    def __init__(self):
        self.action_client = actionlib.SimpleActionClient('/move_base/move',MoveBaseAction)
        self.action_client.wait_for_server(rospy.Duration(action_wait_timeout))


        print 'act_lib_load_end'

    def move(self , pose , timeout=0.0 , ref_frame_id=None):
        _validate_timeout(timeout)

        if ref_frame_id is None:
            ref_frame_id = 'map'

        target_pose = PoseStamped()
        target_pose.header.frame_id = ref_frame_id
        target_pose.header.stamp = rospy.Time(0)
        target_pose.pose = geometry.tuples_to_pose(pose)
        goal = MoveBaseGoal()
        goal.target_pose = target_pose
        self.action_client.send_goal(goal)

    def go(self, x, y, yaw, timeout=0.0, relative=False):
       _validate_timeout(timeout)

       position = geometry.Vector3(x, y, 0)
       quat = tf.transformations.quaternion_from_euler(0, 0, yaw)
       orientation = geometry.Quaternion(*quat)
       pose = (position, orientation)

       if relative:
           ref_frame_id = 'base_footprint'
           print 'base_footprint'
       else:
           ref_frame_id = 'map'
           print 'map'
       self.move(pose, timeout, ref_frame_id)
