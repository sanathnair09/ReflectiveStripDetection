import cv2
import numpy as np
import Detection


cap = cv2.VideoCapture(0)

HUE = 60
THRESHOLD = 25

lower_green = np.array([HUE-THRESHOLD, 100, 40])
upper_green = np.array([HUE+THRESHOLD, 225, 255])

detect = Detection(cap.get(3), cap.get(4),  lower_green, upper_green, 5, 2)

while(True):
    _, frame = cap.read()
    # detect.process(frame)
    pixelWidth = 0
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # detect.calibrateCamera(frame, 39.5)
    pixel_width = 0
    if(len(contours) > 0):
        for cntr in contours:
            area = cv2.contourArea(cntr)
            if (area > 400):
                rect = cv2.minAreaRect(cntr)
                box = cv2.boxPoints(rect)
                box = np.int0(box)  # box[0] bottom most point
                x_coords = box[:, 0]
                pixel_width = np.max(x_coords) - np.min(x_coords)

    dist = detect.distanceToObject(pixelWidth=pixel_width)
    print("dist", dist)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
