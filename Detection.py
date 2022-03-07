import cv2
import numpy as np
import json

# DRAWING CONSTANTS
BBOX_COLOR = (227, 5, 216)
AREA_THRESHOLD = 400
RADIUS = 10
COLOR = (255, 0, 0)
THICKNESS = -1


class Detection:

    def __init__(self,  frame_width: float, frame_height: float, hsv_lower: np.ndarray,
                 hsv_upper: np.ndarray, tracker_width: float, tracker_height: float,
                 area_threshold_min=400, area_threshold_max=400):

        # camera info
        self.FRAME_WIDTH = frame_width  # float `width`
        self.FRAME_HEIGHT = frame_height

        # misc
        self.area_threshold_min = area_threshold_min
        self.area_threshold_max = area_threshold_max

        # HSV paramaters
        self.hsv_lower = hsv_lower
        self.hsv_upper = hsv_upper

        # tracker info
        self.tracker_width = tracker_width
        self.tracker_height = tracker_height

        self.focalLength = 1410

    def getMask(self, frame: any) -> any:
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # (OPTIONAL) blurring (idk if it helps, maybe useful for webcam/jevois)
        # blurred = cv2.GaussianBlur(frame, (5, 5), 0)
        # hsv_blurred = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        # using the lower and upper HSV thresholds and filtering out whatever doesn't fall in the threshold
        mask = cv2.inRange(hsv, self.hsv_lower, self.hsv_upper)

        # (OPTIONAL) blurred mask
        # mask_blurred = cv2.inRange(hsv_blurred, lower_green, upper_green)
        return mask

    def getContours(self, mask, visible=False):
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

                    rect = cv2.minAreaRect(cntr)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)  # box[0] bottom most point

                    if visible:
                        cv2.drawContours(mask, [box], 0, BBOX_COLOR, 4)
        return filtered_contours, cX, cY

    def process(self, frame: any) -> bool or None:
        mask = self.getMask(frame)
        # finding contours in the image (its an inbuilt opencv2 function)
        filtered_contours, cX, cY = self.getContours(mask)

        if (len(filtered_contours) > 1):
            cX = int(cX/len(filtered_contours))
            cY = int(cY/len(filtered_contours))
            center_coordinates = (cX, cY)

            # Using cv22.circle() method
            cv2.circle(mask, center_coordinates, RADIUS, COLOR, THICKNESS)

        # showing what camera sees and output of HSV filtered frames
        # cv2.imshow("original", frame)
        cv2.imshow("filtered", mask)
        self.cX = cX
        self.cY = cY

    def angleToTurn() -> float:
        pass

    def distanceToObject(self, pixelWidth: float) -> float or bool:
        if(pixelWidth == 0):
            return 0
        return (self.tracker_width * self.focalLength) / pixelWidth

    def getPixelWidth(self, contours: any) -> float:
        pixel_width = 0
        if(len(contours) > 0):
            for cntr in contours:
                area = cv2.contourArea(cntr)
                if (area > AREA_THRESHOLD):
                    rect = cv2.minAreaRect(cntr)
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)  # box[0] bottom most point
                    x_coords = box[:, 0]
                    pixel_width = np.max(x_coords) - np.min(x_coords)
        return pixel_width

    def calibrateCamera(self, frame: any, known_distance: float) -> bool:
        # Focal Length = (Pixel Width * Known Distance) / Known Width
        mask = self.getMask(frame)
        filtered_contours = self.getContours(mask)
        pixel_width = self.getPixelWidth(filtered_contours)
        focalLength = (pixel_width * known_distance) / self.tracker_width
        self.focalLength = focalLength
        return focalLength