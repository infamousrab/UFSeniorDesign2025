# wifiService.py
import socket
import threading
import numpy as np
import cv2
from picamera2 import Picamera2
import movement
import detectionTest

HOST = '0.0.0.0'
PORT_IMAGE, PORT_SENSOR = 12345, 12346
WIDTH, HEIGHT = 320, 240

# Initialize camera once
picam2 = Picamera2()
picam2.start()

def rgb888_to_rgb565(img_rgb: np.ndarray) -> bytes:
    r = (img_rgb[..., 0] >> 3).astype(np.uint16)
    g = (img_rgb[..., 1] >> 2).astype(np.uint16)
    b = (img_rgb[..., 2] >> 3).astype(np.uint16)
    return ((r << 11) | (g << 5) | b).astype('>u2').tobytes()

def handle_image_stream(client):
    print("[WiFi] Image client connected")
    try:
        while True:
            img = detectionTest.process_frame(picam2.capture_array())
            img = cv2.resize(img, (WIDTH, HEIGHT))
            # img = cv2.resize(picam2.capture_array(), (WIDTH, HEIGHT))
            img = cv2.rotate(img, cv2.ROTATE_180)
            client.sendall(f"IMG:{WIDTH},{HEIGHT}\n".encode())
            client.sendall(rgb888_to_rgb565(img))
    except Exception as e:
        print("[WiFi] Image stream error:", e)
    finally:
        client.close()

def handle_sensor_input(client):
    print("[WiFi] Sensor client connected")
    try:
        with client.makefile('r') as stream:
            for line in stream:
                try:
                    b1, b2, b3, b4, p1, p2 = map(int, line.strip().split(','))
                    
                    movement.moverobot(b1, b2, b3, b4, p1, p2)
                    
                    print(f"[WiFi] Buttons: {bool(b1)}, {bool(b2)}, {bool(b3)}, {bool(b4)} | Pots: {p1}, {p2}")
                except Exception as e:
                    print("[WiFi] Parse error:", e)
    except Exception as e:
        print("[WiFi] Sensor stream error:", e)
    finally:
        client.close()

def start_server(port, handler, name):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, port))
    server.listen(1)
    print(f"[WiFi] {name} server listening on {HOST}:{port}")
    while True:
        try:
            client, addr = server.accept()
            print(f"[WiFi] {name} client connected from {addr}")
            threading.Thread(target=handler, args=(client,), daemon=True).start()
        except Exception as e:
            print(f"[WiFi] {name} server error:", e)

def start_wifi_server():
    threading.Thread(target=start_server, args=(PORT_IMAGE, handle_image_stream, "Image"), daemon=True).start()
    threading.Thread(target=start_server, args=(PORT_SENSOR, handle_sensor_input, "Sensor"), daemon=True).start()
