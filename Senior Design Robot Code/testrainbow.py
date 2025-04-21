import asyncio
import motors
from bleak import BleakClient
import cv2
import numpy as np
from picamera2 import Picamera2

width=320
height=240

img = np.zeros((height, width, 3), dtype=np.uint8)

for y in range(height):
    # Generate color using HSV to RGB mapping
    hue = int((y / height) * 180)  # OpenCV uses hue range [0, 180]
    hsv_color = np.full((1, width, 3), (hue, 255, 255), dtype=np.uint8)
    rgb_row = cv2.cvtColor(hsv_color, cv2.COLOR_HSV2BGR)
    img[y] = rgb_row

# Rotate 180 degrees to match display orientation
img = cv2.rotate(img, cv2.ROTATE_180)

cv2.imwrite("rainbow_test.png", img)