#!/usr/bin/env python
#-*- coding:utf-8 -*-

#from common import world_champ#横山さんお手製基本情報ぶっ込むパッケージ
import hsrb_interface
import rospy
from sensor_msgs.msg import LaserScan
import tf, math
import numpy as np
from std_msgs import String
#現状このくらいで。

robot = hsrb_interface.Robot()
omni_base = robot.get("omni_base")
tts = robot.get('default', robot.Items.TEXT_TO_SPEECH)
tts.language=tts.ENGLISH
#腕とか使わないから、現状"whole_body""gripper"入れてない。

#""" commonがわかったら消すから勘弁して。
#map_data={"start":(x,y),"waypoint":(x,y),"exit":(x,y)}
#"""

ranges=[]
meanDist=0.0
maxDist=-100.0
minDist= 100.0

door_flag = False
waitalk_flag = False

def scanLaser(data):
    global ranges
    ranges=data.ranges
    mid_index = len(data.ranges) // 2
    dists = [val for val in ranges[mid_index-10:mid_index+10]
           if not math.isnan(val)]
    if len(dists) != 0:
      global meanDist
      meanDist =  np.mean(dists)
      global maxDist
      maxDist = np.max(dists)
      global minDist
      minDist = np.min(dists)
      global door_flag
      if door_flag == False:
         rospy.loginfo('range:min mean min >'+str(minDist)+' '+str(meanDist)+' '+str(maxDist))

def talk_reserver(talkdata):
    global waitalk_flag
    if talkdata.data == ("ok"or"continue"or"Go exit"):
       waitalk_flag = True

class Inspection():
      def __init__(self):
          #ここに、手押しやらなにかほちぃ。
          listener = tf.TransformListener()
          now = rospy.Time(0)
          rospy.sleep(1)
          #TFが来るまで待つ(Marker見せるまでをイメージしてる。)
          print "wait for ar_marker"
          tts.say("please look for me a r marker")
          try:
             listener.waitForTransform("/head_l_stereo_camera_frame", "/ar_marker/15", now, rospy.Duration(1000.0))#ar_marker/15が見つかるまで待つ。
          except  (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
               print "marker not found"
               tts.say("sorry I can't find")
          rospy.Subscriber("/hsrb/base_scan",LaserScan,scanLaser, queue_size=1)
          # Wait door open
          while not rospy.is_shutdown():
                if meanDist > 2.0:
                   print "door is now open!!"
                   global door_flag
                   door_flag = True
                   break
                rospy.sleep(0.1)

          rospy.sleep(1.0)
          tts.say("erasers inspection start")

           """
           #位置補正はここかな
           """
#           self.main() #まだ実装してないので止。

      def main(self):
          omni_base.go(0.2,0.0,0.0,relative=True)#アリーナ侵入
          tts.say("I wanna go waypoint")#waypointというのは変えて頂戴な。
          rospy.sleep(4.0)
          while not rospy.is_shutdown(): #HSRが！
                                         #waypointに行くまで！！
                                         #回すのをやめない！！！
                try:
                  omni_base.go(,,)#waypoint
                  break
                except:
                   continue
          rospy.Subscriber("/talk_stopper",String,talk_reserver, queue_size=1)
          while not rospy.is_shutdown(): #君が!
                                         #Yes とかGo exitとか、continueと言うまで！！
                                         #止まるのをやめない！！！
                 global waitalk_flag
                 if waitalk_flag == True:
                    tts.say("I wanna go exit")
                    rospy.sleep(1.0)
                    break
          tts.say("please check emergency button")
          while not rospy.is_shutdown(): #HSRが！
                                         #waypointに行くまで！！
                                         #回すのをやめない！！！
                try:
                  omni_base.go(,,)#exit
                  break
                except:
                   continue
          
if __name__ == "__main__":
   Inspection()
   rospy.spin()
