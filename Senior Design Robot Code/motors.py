import pigpio

# Initialize pigpio once
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Failed to connect to pigpio daemon")

class DCMotor:
    def __init__(self, pi, forward_pin, reverse_pin, encoder_a_pin, encoder_b_pin):
        self.pi = pi
        self.forward_pin = forward_pin
        self.reverse_pin = reverse_pin
        self.encoder_a_pin = encoder_a_pin
        self.encoder_b_pin = encoder_b_pin

        # Set GPIO modes
        self.pi.set_mode(self.forward_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.reverse_pin, pigpio.OUTPUT)
        self.pi.set_mode(self.encoder_a_pin, pigpio.INPUT)
        self.pi.set_mode(self.encoder_b_pin, pigpio.INPUT)

    def set(self, speed, direction):
        """Set the motor speed and direction. 1=forward, 0=reverse."""
        duty_cycle = int(speed * 255 / 100)  # Convert speed to duty cycle (0-255)
        
        if direction:
            self.pi.set_PWM_dutycycle(self.forward_pin, duty_cycle)
            self.pi.set_PWM_dutycycle(self.reverse_pin, 0)
        else:
            self.pi.set_PWM_dutycycle(self.forward_pin, 0)
            self.pi.set_PWM_dutycycle(self.reverse_pin, duty_cycle)
            
    def stop(self):
        """Stop the motor."""
        self.pi.set_PWM_dutycycle(self.forward_pin, 0)
        self.pi.set_PWM_dutycycle(self.reverse_pin, 0)
        
# GPIO Pin Definitions

# Initialize motors
rightDrive = DCMotor(pi, 12, 18, 23, 24)
leftDrive = DCMotor(pi, 19, 13, 14, 15)
intake = DCMotor(pi, 26, 11, 27, 27)
binClamp = DCMotor(pi, 9, 10, 25, 8)

# Linear Actuator
binLiftStep = 20
binLiftDirection = 21

# IMU
imuData = 2
imuClock = 3
imuInterrupt = 4

# Speaker
speakerPin = 17

# Power Button
powerButton = 7

# Unused Pins (Reserved for Future Use)
#unusedPin1 = 0
# unusedPin2 = 27
# unusedPin3 = 22
# unusedPin4 = 5
# unusedPin5 = 6