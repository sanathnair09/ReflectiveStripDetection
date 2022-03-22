import socket
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

HUE = 100
# HUE threshold (how much above and below the actual color we are trying to detect)
THRESHOLD = 25

LOWER_GREEN = np.array([HUE-THRESHOLD, 100, 100])
UPPER_GREEN = np.array([HUE+THRESHOLD, 225, 255])

AREA_THRESHOLD = 500

UDP_IP = "localhost"
UDP_PORT = 8080

while True:
    _, frame = cap.read()
    # convert the frame from BGR to HSV
    # opencv2 uses BGR instead of RGB because of some stupid reason
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # (OPTIONAL) blurring (idk if it helps, maybe useful for webcam/jevois)
    # blurred = cv2.GaussianBlur(frame, (5, 5), 0)
    # hsv_blurred = cv2.cv2tColor(blurred, cv2.COLOR_BGR2HSV)

    # threshold values for green
    # opencv2 havles the HUE constant so instead of being from 0 to 360 its 0 to 180
    # try and keep satuaration and values as low as possible to remove noise although increasing the threshold will allow for higher chance of detection

    # using the lower and upper HSV thresholds and filtering out whatever doesn't fall in the threshold
    mask = cv2.inRange(hsv, LOWER_GREEN, UPPER_GREEN)

    # (OPTIONAL) blurred mask
    # mask_blurred = cv2.inRange(hsv_blurred, lower_green, upper_green)

    # finding contours in the image (its an inbuilt opencv2 function)
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []
    cX, cY = 0, 0
    # making sure contour exists
    if(len(contours) > 1):
        for cntr in contours:
            area = cv2.contourArea(cntr)
            if (area > AREA_THRESHOLD):
                filtered_contours.append(cntr)

                M = cv2.moments(cntr)
                cX += int(M["m10"] / M["m00"])
                cY += int(M["m01"] / M["m00"])
            

    if len(filtered_contours) > 1:
        cX = int(cX/len(filtered_contours))
        cY = int(cY/len(filtered_contours))
        center_coordinates = (cX, cY)
        print(center_coordinates)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = (UDP_IP, UDP_PORT)
    sock.bind(info)
    data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
    print("received message: %s" % data)

    # MESSAGE=f"{cX}:{cY}"
    # sock.sendto(bytes(MESSAGE), info)
    # cX, cY = 0, 0
