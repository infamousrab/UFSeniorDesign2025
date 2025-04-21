import cv2
import numpy as np

def process_frame(frame):
    # Convert to HSV for purple detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)

    # Define purple range
    lower_purple = np.array([120, 80, 100])
    upper_purple = np.array([160, 255, 255])
    mask = cv2.inRange(hsv, lower_purple, upper_purple)

    # Morphological cleanup
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # Find contours of purple areas
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(cnt)
            # Draw a red box (BGR)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Return annotated image
    return frame
