from pyo import *
import time
import random

s = Server(sr=44100, nchnls=2)
s.setInOutDevice(13)
s.boot()

pa_list_devices()

pitches = [midiToHz(m) for m in [36, 43, 48, 55, 60, 62, 64, 65, 67, 69, 71, 72]]

# Create a white noise generator.
noise = Noise()

# Use a low-pass filter to soften the noise and give it a "wind" characteristic.
# Adjust the frequency to change the character of the wind.
filt = ButLP(noise).out()

# LFO to modulate filter frequency
lfo = Sine(freq=0.1, mul=100, add=500)
filt.freq = lfo

# Reverb for spatial effect
rev = Freeverb(filt).out()

# Define a function to randomly change parameters at each step
def randomize():
   
    noise.setMul(random.uniform(0.5, 1))

    # Randomly change the frequency and resonance of the low-pass filter
    filt.freq = random.uniform(1000, 1000)
    filt.Q = random.uniform(1, 5)

    # Randomly change the LFO rate
    lfo.freq = random.uniform(0.1, 0.2)

    # Randomly change reverb parameters
    rev.roomsize = random.uniform(0.4, 0.9)
    rev.damp = random.uniform(0.4, 0.5)

    # Schedule the next call to this function
    CallAfter(randomize, time=random.uniform(2, 3))



# Start the randomization process
randomize()

# Start the server
s.start()

# Keep the script running for a specified duration
try:
    # Run for a certain duration (e.g., 30 seconds)
    #time.sleep(30)
    # Start the randomization process
    while True:
        randomize()
        time.sleep(0.1)
except KeyboardInterrupt:
    pass

# Stop the server
s.stop()
