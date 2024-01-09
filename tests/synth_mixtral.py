# Import necessary modules
from pyo import *
import time
import threading

# Initialize Pyo server with default audio settings (48000 Hz, stereo)
s = Server(duplex=0)
s.setInOutDevice(13)
s.boot()


# Load the wind noise sample
sfplayer = SfPlayer("wind_noise.wav").out()

# Apply a low-pass filter to the output of the sfplayer
filt = Biquad("lowpass", freq=500, q=0.1)
filt.setInput(sfplayer)
filt.out()

# Create an envelope to control the amplitude of the sound over time
env = AdEnv(attack=3, decay=4, sustain=0.5, release=6).play()

# Connect the envelope to the output of the filter
filt >> env.mix(1)

# Start the server and let it run for a while
s.start()
time.sleep(10)
s.stop()
