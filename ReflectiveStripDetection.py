# import cv2 as cv
# import numpy as np

# # video input device
# cap = cv.VideoCapture(0)

# BBOX_COLOR = (227, 5, 216)

# AREA_THRESHOLD = 400
# RADIUS = 10
# COLOR = (255, 0, 0)
# THICKNESS = -1

# FRAME_WIDTH = cap.get(3)  # float `width`
# FRAME_HEIGHT = cap.get(4)  # float `height`

# TRACKER_WIDTH = 5  # inch
# TRACKER_HEIGHT = 2  # inch

# FOCAL_LENGTH = 0

# # focal length = (px_width * distance_from_camera) / object_width


# def calculateFocalLength(P, D, W):
#     return (P * D) / W


# # the color lol
# HUE = 100
# # HUE threshold (how much above and below the actual color we are trying to detect)
# THRESHOLD = 25

# lower_green = np.array([HUE-THRESHOLD, 100, 100])
# upper_green = np.array([HUE+THRESHOLD, 225, 255])


# def calculateDistance(focalLength, px_width):
#     return ()


# while True:
#     # get frame from camera
#     _, frame = cap.read()
#     # convert the frame from BGR to HSV
#     # opencv uses BGR instead of RGB because of some stupid reason
#     hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

#     # (OPTIONAL) blurring (idk if it helps, maybe useful for webcam/jevois)
#     # blurred = cv.GaussianBlur(frame, (5, 5), 0)
#     # hsv_blurred = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

#     # threshold values for green
#     # opencv havles the HUE constant so instead of being from 0 to 360 its 0 to 180
#     # try and keep satuaration and values as low as possible to remove noise although increasing the threshold will allow for higher chance of detection

#     # using the lower and upper HSV thresholds and filtering out whatever doesn't fall in the threshold
#     mask = cv.inRange(hsv, lower_green, upper_green)

#     # (OPTIONAL) blurred mask
#     # mask_blurred = cv.inRange(hsv_blurred, lower_green, upper_green)

#     # finding contours in the image (its an inbuilt opencv function)
#     contours, _ = cv.findContours(
#         mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

#     filtered_contours = []
#     cX, cY = 0, 0
#     # making sure contour exists
#     if(len(contours) > 1):
#         for cntr in contours:
#             area = cv.contourArea(cntr)
#             if (area > AREA_THRESHOLD):
#                 filtered_contours.append(cntr)

#                 M = cv.moments(cntr)
#                 cX += int(M["m10"] / M["m00"])
#                 cY += int(M["m01"] / M["m00"])
#                 rect = cv.minAreaRect(cntr)
#                 box = cv.boxPoints(rect)
#                 box = np.int0(box)  # box[0] bottom most point
#                 # print(box[:, 0])
#                 # print(np.max(box[:, 0]) - np.min(box[:, 0]))

#                 # cv.circle(mask, [box[0][0], box[0][1]], RADIUS, BBOX_COLOR, 5)
#                 # cv.circle(mask, [box[1][0], box[1][1]], RADIUS, BBOX_COLOR, 2)

#                 cv.drawContours(mask, [box], 0, BBOX_COLOR, 4)

#     if len(filtered_contours) > 1:
#         cX = int(cX/len(filtered_contours))
#         cY = int(cY/len(filtered_contours))
#         center_coordinates = (cX, cY)
#         # Using cv2.circle() method
#         cv.circle(mask, center_coordinates, RADIUS, COLOR, THICKNESS)

#     # showing what camera sees and output of HSV filtered frames
#     # cv.imshow("original", frame)
#     cv.imshow("hsv", hsv)

#     cv.imshow("filtered", mask)
#     cX, cY = 0, 0
#     # kill if escape is pressed
#     k = cv.waitKey(5) & 0xFF
#     if k == 27:
#         break

# cv.destroyAllWindows()
