import cv2
import numpy as np
from picamera2 import Picamera2

def bgr_to_rgb565(img_bgr):
    """
    Convert a BGR image (OpenCV) to RGB565 format.
    Output: NumPy array of shape (H, W) with dtype=np.uint16
    """
    b = img_bgr[:, :, 0] >> 3  # 5 bits
    g = img_bgr[:, :, 1] >> 2  # 6 bits
    r = img_bgr[:, :, 2] >> 3  # 5 bits

    rgb565 = (r << 11) | (g << 5) | b
    return rgb565.astype(np.uint16)

# === STEP 1: Init camera ===
picam2 = Picamera2()
picam2.start()

# === STEP 2: Capture and resize ===
frame = picam2.capture_array()
resized = cv2.resize(frame, (320, 240))
resized = cv2.rotate(resized, cv2.ROTATE_180)

# === STEP 3: Remove alpha channel if present ===
if resized.shape[2] == 4:
    resized_bgr = resized[:, :, :3]
else:
    resized_bgr = resized

# === STEP 4: Convert to RGB565 ===
rgb565_array = bgr_to_rgb565(resized_bgr)

# === STEP 5: Print RGB565 values (as hex) ===
# print("RGB565 data (hex values, row 0):")
# print([f"0x{val:04X}" for val in rgb565_array[0]])

# === STEP 6: Show final image ===
# Convert BGR to RGB for display
resized_rgb = cv2.cvtColor(resized_bgr, cv2.COLOR_BGR2RGB)
cv2.imwrite("resized_rgb.jpg", resized_rgb)

