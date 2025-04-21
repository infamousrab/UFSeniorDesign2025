import initinit
import motors
import pigpio
import time
import math
import speaker

# Constants
ADC_MIN, ADC_MAX = 0, 65535
OUTPUT_MIN, OUTPUT_MAX = -100, 100
CENTER_P1, CENTER_P2 = 29550, 35512
DEADZONE_THRESHOLD = 1500
SPEED_SCALE = 0.5
DEBOUNCE_DELAY = 0.1
CLAMP_THRESHOLD = 20

# Global control state
intake_on = False
controls = "tank"

# Button debounce state
prev_b1 = prev_b2 = prev_b3 = prev_b4 = 0
last_b1_toggle_time = last_b2_toggle_time = last_b3_toggle_time = last_b4_toggle_time = 0

def initmotors():
    motors.leftDrive.stop()
    motors.rightDrive.stop()
    motors.intake.stop()
    motors.binClamp.stop()

def map_adc(value, center, deadzone, in_min=ADC_MIN, in_max=ADC_MAX, out_min=OUTPUT_MIN, out_max=OUTPUT_MAX):
    if abs(value - center) < deadzone:
        return 0
    return ((value - center) / (in_max - center) * out_max) if value > center else ((value - center) / (center - in_min)) * -out_min

def moverobot(b1, b2, b3, b4, raw_p1, raw_p2):
    global intake_on
    global prev_b1, prev_b2, prev_b3, prev_b4
    global last_b1_toggle_time, last_b2_toggle_time, last_b3_toggle_time, last_b4_toggle_time

    current_time = time.monotonic()
    button_state = (b4 << 3) | (b3 << 2) | (b2 << 1) | b1
    p1 = map_adc(raw_p1, CENTER_P1, DEADZONE_THRESHOLD)
    p2 = map_adc(raw_p2, CENTER_P2, DEADZONE_THRESHOLD)

    if button_state != 0:
        motors.leftDrive.stop()
        motors.rightDrive.stop()

        # Button 1 – Toggle intake
        if button_state == 0b0001:
            if prev_b1 == 0 and (current_time - last_b1_toggle_time) > DEBOUNCE_DELAY:
                intake_on = not intake_on
                last_b1_toggle_time = current_time
                motors.intake.set(100, 1) if intake_on else motors.intake.stop()
            prev_b1 = 1
        else:
            prev_b1 = 0

        # Button 2 – Potentiometer-controlled clamp
        if button_state == 0b0010:
            if p2 > CLAMP_THRESHOLD:
                motors.binClamp.set(100, 0)
            elif p2 < -CLAMP_THRESHOLD:
                motors.binClamp.set(100, 1)
            else:
                motors.binClamp.stop()
            motors.intake.stop()
            prev_b1 = 0

        # Button 3 – Toggle speaker tone
        if button_state == 0b0100:
            if prev_b3 == 0 and (current_time - last_b3_toggle_time) > DEBOUNCE_DELAY:
                speaker.start_tone(50) if not speaker.running else speaker.stop_tone()
                motors.intake.stop()
                motors.binClamp.stop()
                last_b3_toggle_time = current_time
            prev_b3 = 1
        else:
            prev_b3 = 0

        # Button 4 – Stop everything (or assign other functionality)
        if button_state == 0b1000:
            if prev_b4 == 0 and (current_time - last_b4_toggle_time) > DEBOUNCE_DELAY:
                speaker.start_tone(150) if not speaker.running else speaker.stop_tone()
                motors.intake.stop()
                motors.binClamp.stop()
                last_b4_toggle_time = current_time
            prev_b4 = 1
        else:
            prev_b4 = 0
    else:
        # No buttons pressed
        motors.binClamp.stop()

        # Reset all button states
        prev_b1 = prev_b2 = prev_b3 = prev_b4 = 0

        # Normalize vector
        magnitude = math.sqrt(p1**2 + p2**2)
        if magnitude > 100:
            scale = 100 / magnitude
            p1 *= scale
            p2 *= scale

        left_speed = max(min((p1 + p2) * SPEED_SCALE, 100), -100)
        right_speed = max(min((p1 - p2) * SPEED_SCALE, 100), -100)

        motors.leftDrive.set(abs(left_speed), 1 if left_speed >= 0 else 0)
        motors.rightDrive.set(abs(right_speed), 1 if right_speed >= 0 else 0)
