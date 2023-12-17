import numpy as np
from noise import pnoise1
import sounddevice as sd

# Parameters
sample_rate = 44100
duration = 12  # seconds
wind_speed = 0.5  # Adjust this for different wind speeds

# Generate Perlin noise-based wind sound
def generate_wind_sound(duration, wind_speed):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    sound = np.zeros_like(t)
    for i, ti in enumerate(t):
        sound[i] = pnoise1(ti * wind_speed)
    return sound

# Stream the sound in real-time
def callback(outdata, frames, time, status):
    outdata[:] = generate_wind_sound(frames / sample_rate, wind_speed).reshape(-1, 1)

# Start streaming
with sd.OutputStream(callback=callback, samplerate=sample_rate, channels=1):
    sd.sleep(int(duration * 1000))
