import numpy as np
import Temp
import cv2

cap = cv2.VideoCapture(0)

HUE = 100
THRESHOLD = 25

lower_green = np.array([HUE-THRESHOLD, 100, 40])
upper_green = np.array([HUE+THRESHOLD, 225, 255])


detect = Temp(cap, cap.get(3), cap.get(4),  lower_green, upper_green, 5)
# detect.calibrate(9.25)
# x = 0
# while(x < 100000000):
#     angle, dist = detect.periodic()
