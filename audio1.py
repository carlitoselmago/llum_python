from pyo import *
import random
import time

# Initialize Pyo server
s = Server().boot()

# Load audio files
audio1 = SfPlayer('audio1.mp3', loop=True)
audio2 = SfPlayer('audio2.mp3', loop=True)

# Apply reverb to audio1
rev = Freeverb(audio1, size=0.8, damp=0.7, bal=0.5).out()

# Apply filter to audio1
filt = ButBP(audio1, freq=1000, q=5).out()

# Volume control
vol1 = SigTo(value=0.5, time=0.1, init=0.5)
vol2 = SigTo(value=0.5, time=0.1, init=0.5)
audio1.mul = vol1
audio2.mul = vol2

# Start the server
s.start()

# Function to randomly change parameters
def randomize():
    # Randomize reverb dry/wet
    rev.bal = random.uniform(0, 1)
    
    # Randomize filter frequency
    filt.freq = random.uniform(60, 20000)
    
    # Randomize volumes
    vol1.value = random.uniform(0.1, 1)
    vol2.value = random.uniform(0.1, 1)

# Loop to change parameters every 5 seconds
while True:
    randomize()
    time.sleep(5)
