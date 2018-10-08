#!/usr/bin/env python

import threading

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2

# Super simple USB camera driver for ROS1, using OpenCV
# TODO publish calibration data in a camera info message


class CameraTest():

    def __init__(self):
        rospy.init_node('usb_camera_node', anonymous=False)

        self._image_pub = rospy.Publisher('image_raw', Image, queue_size=1)
        self._cv_bridge = CvBridge()

        self._video_thread = None
        self._stop_request = None

    def start(self):
        rospy.loginfo("starting video thread")
        self._stop_request = threading.Event()
        self._video_thread = threading.Thread(target=self.video_worker)
        self._video_thread.start()

    def stop(self):
        rospy.loginfo("stopping video thread")
        self._stop_request.set()
        self._video_thread.join(timeout=2)
        self._stop_request = None
        self._video_thread = None

    def video_worker(self):
        cap = cv2.VideoCapture(0)

        frame_num = 0
        while not self._stop_request.isSet():
            ret, frame = cap.read()

            # Publish at 1Hz to reduce CPU usage
            frame_num += 1
            if frame_num == (30-1):
                self._image_pub.publish(self._cv_bridge.cv2_to_imgmsg(frame, 'bgr8'))
                frame_num = 0

            cv2.imshow('frame', frame)
            cv2.waitKey(1)

        cap.release()
        cv2.destroyAllWindows()


def main(args=None):
    node = CameraTest()

    try:
        node.start()
        rospy.spin()
    except KeyboardInterrupt:
        rospy.loginfo("Ctrl-C detected, shutting down")
        node.stop()


if __name__ == '__main__':
    main()
