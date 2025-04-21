import uasyncio as asyncio
import network
from machine import Pin, SPI, ADC
import ili9341

# WiFi + Server
SSID = "Marville_2.4GHz"
PASSWORD = "IronManRIP2019"
SERVER_IP = "192.168.1.138"
PORT_IMAGE, PORT_SENSOR = 12345, 12346

# Display
spi = SPI(0, baudrate=32000000, sck=Pin(18), mosi=Pin(19))
display = ili9341.ILI9341(spi, cs=Pin(17), dc=Pin(20), rst=Pin(21), w=320, h=240, r=3)

# Inputs
buttons = [Pin(i, Pin.IN, Pin.PULL_UP) for i in range(2, 6)]
pots = [ADC(0), ADC(1)]

# Status LEDs
led_green = Pin(1, Pin.OUT)
led_red = Pin(0, Pin.OUT)

# LED control state
status = {
    'wifi_connected': False,
    'talking_to_pi': False,
}

async def led_status_loop():
    while True:
        if not status['wifi_connected']:
            led_red.on()
            led_green.off()
            await asyncio.sleep(0.2)
        elif status['wifi_connected'] and not status['talking_to_pi']:
            led_green.off()
            led_red.toggle()
            await asyncio.sleep(0.5)
        elif status['wifi_connected'] and status['talking_to_pi']:
            led_red.off()
            led_green.on()
            await asyncio.sleep(0.5)

async def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        wlan.connect(SSID, PASSWORD)
        print("[Pico] Connecting to WiFi...")
        for _ in range(20):
            if wlan.isconnected():
                print("[Pico] WiFi connected:", wlan.ifconfig())
                status['wifi_connected'] = True
                return True
            await asyncio.sleep(0.5)
        print("[Pico] WiFi connection failed")
        status['wifi_connected'] = False
        return False
    status['wifi_connected'] = True
    return True

async def receive_image_loop():
    while True:
        try:
            reader, writer = await asyncio.open_connection(SERVER_IP, PORT_IMAGE)
            print("[Pico] Connected to image stream")
            status['talking_to_pi'] = True

            while True:
                try:
                    header = await asyncio.wait_for(reader.readline(), timeout=5)
                    if not header.startswith(b'IMG:'):
                        continue
                    w, h = map(int, header.decode().strip().split(':')[1].split(','))
                    buf = bytearray(w * h * 2)
                    view = memoryview(buf)
                except asyncio.TimeoutError:
                    raise Exception("Timeout waiting for image header")
                except Exception as e:
                    print("[Pico] Header parse error:", e)
                    continue

                read = 0
                while read < len(buf):
                    try:
                        n = await asyncio.wait_for(reader.readinto(view[read:]), timeout=2)
                        if n == 0:
                            raise Exception("Connection closed during image")
                        read += n
                    except asyncio.TimeoutError:
                        raise Exception("Timeout reading image data")

                display._writeblock(0, 0, w - 1, h - 1, buf)

        except Exception as e:
            print("[Pico] Image error:", e)
            status['talking_to_pi'] = False
            await asyncio.sleep(2)

async def send_sensor_loop():
    while True:
        try:
            reader, writer = await asyncio.open_connection(SERVER_IP, PORT_SENSOR)
            print("[Pico] Connected to sensor stream")
            status['talking_to_pi'] = True
            while True:
                btns = [str(int(not b.value())) for b in buttons]
                pots_vals = [str(pots[0].read_u16()), str(65535 - pots[1].read_u16())]
                msg = ",".join(btns + pots_vals) + "\n"
                writer.write(msg.encode())
                await writer.drain()
                await asyncio.sleep(0.1)
        except Exception as e:
            print("[Pico] Sensor error:", e)
            status['talking_to_pi'] = False
            await asyncio.sleep(2)

async def main():
    try:
        asyncio.create_task(led_status_loop())
        if await connect_wifi():
            asyncio.create_task(receive_image_loop())
            asyncio.create_task(send_sensor_loop())
            while True:
                await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("[Pico] KeyboardInterrupt — shutting down")
    finally:
        print("[Pico] Done.")

try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("[Pico] Exiting asyncio event loop")
