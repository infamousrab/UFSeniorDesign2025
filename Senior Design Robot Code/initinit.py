import pigpio
import movement
import audio

# Initialize pigpio once
pi = pigpio.pi()
if not pi.connected:
    raise Exception("Failed to connect to pigpio daemon")

def init():
    
    audio.audio_init()
    movement.initmotors()
    