# TODO typing functions and stuff bc i didn't cuz i lazy and ghetto like that
import cv2
import numpy as np

# DRAWING CONSTANTS
BBOX_COLOR = (227, 5, 216)
AREA_THRESHOLD = 400
RADIUS = 10
COLOR = (255, 0, 0)
THICKNESS = -1


class Temp:
    def __init__(self,  cap: any, frame_width: float, frame_height: float, hsv_lower: np.ndarray,
                 hsv_upper: np.ndarray, tracker_width: float, tracker_height: float,
                 area_threshold_min=400, area_threshold_max=400):
        # camera info
        self.cap = cap
        self.FRAME_WIDTH = frame_width  # float `width`
        self.FRAME_HEIGHT = frame_height

        # misc
        self.area_threshold_min = area_threshold_min
        self.area_threshold_max = area_threshold_max
        self.focalLength = 0

        # HSV paramaters
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper

        # tracker info
        self.tracker_width = tracker_width
        self.tracker_height = tracker_height

        # self.focalLength = 1410

    def perioidic(self):
        center_coords, pxWidth = self.findTarget()
        distanceToTarget = self.distanceToObject(pxWidth=pxWidth)
        angleToTurn = self.angleToTurn(center_coords[0], distanceToTarget)
        return angleToTurn, distanceToTarget

    def findTarget(self, display=False):
        _, frame = self.cap.read()
        # convert the frame from BGR to HSV
        # opencv uses BGR instead of RGB because of some stupid reason
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # (OPTIONAL) blurring (idk if it helps, maybe useful for webcam/jevois)
        # blurred = cv.GaussianBlur(frame, (5, 5), 0)
        # hsv_blurred = cv.cvtColor(blurred, cv.COLOR_BGR2HSV)

        # threshold values for green
        # opencv havles the HUE constant so instead of being from 0 to 360 its 0 to 180
        # try and keep satuaration and values as low as possible to remove noise although increasing the threshold will allow for higher chance of detection

        # using the lower and upper HSV thresholds and filtering out whatever doesn't fall in the threshold
        mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)
        # (OPTIONAL) blurred mask
        # mask_blurred = cv.inRange(hsv_blurred, lower_green, upper_green)

        # finding contours in the image (its an inbuilt opencv function)
        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cX, cY, contourCount, pxWidth = 0
        # making sure contour exists
        if(len(contours) > 1):
            for cntr in contours:
                area = cv2.contourArea(cntr)
                if (area > self.area_threshold_min):
                    contourCount += 1

                    M = cv2.moments(cntr)
                    cX += int(M["m10"] / M["m00"])
                    cY += int(M["m01"] / M["m00"])

                    rect = cv2.minAreaRect(cntr)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)  # box[0] bottom most point

                    x_coords = box[:, 0]
                    pxWidth += np.max(x_coords) - np.min(x_coords)

                    if display:
                        cv2.drawContours(mask, [box], 0, BBOX_COLOR, 4)
        if contourCount > 1:
            cX = int(cX/contourCount)
            cY = int(cY/contourCount)
            pxWidth = pxWidth/contourCount
            center_coordinates = (cX, cY)

            if display:
                cv2.circle(mask, center_coordinates, RADIUS, COLOR, THICKNESS)
        if display:
            cv2.imshow("filtered", mask)
        return center_coordinates, pxWidth

    def distanceToObject(self, pxWidth):
        return ((self.tracker_width * self.focalLength) / pxWidth) if self.focalLength != 0 else -1

    def angleToTurn(self, tX, distance):
        return np.arctan((tX - (self.FRAME_WIDTH / 2)) / distance)

    # some random function we gotta play around with
    def calcRPM(self, tY):
        return tY*25+300

    def calibrateCamera(self, knownDistance, repeatCount=10):
        perceivedFocalLength = 0
        for _ in range(repeatCount):
            _, pxWidth = self.findTarget(pixel_Width=True)
            perceivedFocalLength += (pxWidth *
                                     knownDistance) / self.tracker_width
        self.focalLength = perceivedFocalLength
        return perceivedFocalLength/repeatCount
