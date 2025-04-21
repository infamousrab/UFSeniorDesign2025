from machine import Pin, ADC
import time

# Define buttons as input pins with pull-up resistors
button_pins = [2, 3, 4, 5]
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in button_pins]

# Define potentiometers as analog inputs
pot_pins = [26, 27]  # GP26 = ADC0, GP27 = ADC1
pots = [ADC(pin) for pin in pot_pins]

while True:
    # Read buttons (0 = pressed, 1 = not pressed)
    button_states = [not button.value() for button in buttons]

    # Read potentiometers (0 - 65535 range on Pico)
    pot_values = [pot.read_u16() for pot in pots]

    # Print states
    print(f"Buttons: {button_states} | Pots: {pot_values}")
    
    time.sleep(0.2)
