import pigpio
import time
import threading
import math

PIN = 17
PWM_FREQ = 10000  # 10 kHz carrier
SINE_SAMPLES = 10

pi = pigpio.pi()
running = False
thread = None

# Precompute a sine lookup table scaled to 0–100%
sine_lookup = [int((math.sin(2 * math.pi * i / SINE_SAMPLES) + 1) / 2 * 100) for i in range(SINE_SAMPLES)]

def generate_sine_wave(freq):
    global running
    delay = 1.0 / freq / SINE_SAMPLES

    pi.set_PWM_frequency(PIN, PWM_FREQ)
    pi.set_PWM_range(PIN, 100)  # Use percent-based resolution

    while running:
        for duty in sine_lookup:
            if not running:
                break
            start = time.monotonic()
            pi.set_PWM_dutycycle(PIN, duty)
            
            elapsed = time.monotonic() - start
            sleep_time = max(0, delay - elapsed)
            time.sleep(sleep_time)

def start_tone(freq):
    global running, thread
    if running:
        return
    running = True
    thread = threading.Thread(target=generate_sine_wave, args=(freq,), daemon=True)
    thread.start()

def stop_tone():
    global running
    running = False
    pi.set_PWM_dutycycle(PIN, 0)
