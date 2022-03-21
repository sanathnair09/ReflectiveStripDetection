from networktables import NetworkTables
from cscore import CameraServer

import cv2
import numpy as np

from .Temp import Temp as Detection

SERVER = "10.40.79.2"
WIDTH = 320
HEIGHT = 240


# HUE = 60
# THRESHOLD = 25

# lower_green = np.array([HUE-THRESHOLD, 100, 40])
# upper_green = np.array([HUE+THRESHOLD, 225, 255])

# detect = Detection(cap.get(3), cap.get(4),  lower_green, upper_green, 5, 2)


def main():
    intake = cv2.VideoCapture(0)    

    cs = CameraServer.server
    _, frame = intake.read()

    outputStream = cs.putVideo("Intake", WIDTH, HEIGHT)

    img = np.zeros(shape=(HEIGHT, WIDTH, 3), dtype=np.uint8)
    
