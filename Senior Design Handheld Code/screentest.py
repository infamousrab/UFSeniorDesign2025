# Tested with Pico
from ili9341 import ILI9341, color565
from machine import Pin, SPI
import tt14
import time

# Einige Farben from https://www.hobbyelektroniker.ch/resources/PytEsp20.zip
RED = const(0XF800)  # (255, 0, 0)
GREEN = const(0X07E0)  # (0, 255, 0)
BLUE = const(0X001F)  # (0, 0, 255)
YELLOW = const(0XFFE0)  # (255, 255, 0)
FUCHSIA = const(0XF81F)  # (255, 0, 255)
AQUA = const(0X07FF)  # (0, 255, 255)
MAROON = const(0X8000)  # (128, 0, 0)
DARKGREEN = const(0X0400)  # (0, 128, 0)
NAVY = const(0X0010)  # (0, 0, 128)
TEAL = const(0X0410)  # (0, 128, 128)
PURPLE = const(0X8010)  # (128, 0, 128)
OLIVE = const(0X8400)  # (128, 128, 0)
ORANGE = const(0XFC00)  # (255, 128, 0)
DEEP_PINK = const(0XF810)  # (255, 0, 128)
CHARTREUSE = const(0X87E0)  # (128, 255, 0)
SPRING_GREEN = const(0X07F0)  # (0, 255, 128)
INDIGO = const(0X801F)  # (128, 0, 255)
DODGER_BLUE = const(0X041F)  # (0, 128, 255)
CYAN = const(0X87FF)  # (128, 255, 255)
PINK = const(0XFC1F)  # (255, 128, 255)
LIGHT_YELLOW = const(0XFFF0)  # (255, 255, 128)
LIGHT_CORAL = const(0XFC10)  # (255, 128, 128)
LIGHT_GREEN = const(0X87F0)  # (128, 255, 128)
LIGHT_SLATE_BLUE = const(0X841F)  # (128, 128, 255)
WHITE = const(0XFFFF)  # (255, 255, 255)
BLACK = const(0)

text = 'Hello'
spi = SPI(0, baudrate=32000000, sck=Pin(18), mosi=Pin(19))
display = ILI9341(spi, cs=Pin(17), dc=Pin(20), rst=Pin(21), w=320, h=240, r=3)
print("Test")

# coords: x positive left
# coords: y positive down

display.erase()
display.set_color(WHITE,0)
display.set_font(tt14)
display.set_pos(0,0)
display.print(text)
display.set_pos(0,20)
display.print(text)
display.set_pos(40,20)
display.print(text)
for x in range(0,100):
    display.pixel(2*x,x,BLUE)

time.sleep(1)

# Define basic rainbow colors
RAINBOW_COLORS = [0XF800, 0XFFE0, 0X07E0, 0X07FF, 0X001F, 0XF81F]

spi = SPI(0, baudrate=32000000, sck=Pin(18), mosi=Pin(19))
display = ILI9341(spi, cs=Pin(17), dc=Pin(20), rst=Pin(21), w=320, h=240, r=3)

def cycle_rainbow(display, colors, delay=1):
    while True:
        for color in colors:
            display.fill_rectangle(0, 0, display.width, display.height, color)
            time.sleep(delay)

# Start cycling through the rainbow colors
cycle_rainbow(display, RAINBOW_COLORS)
