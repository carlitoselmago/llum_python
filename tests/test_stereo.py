from pyo import *
from time import sleep

# Initialize Pyo server
s = Server(sr=44100, buffersize=4056,audio = "jack")
sleep(5)
pa_list_devices()
# Set the input/output device to device number 12
s.setInOutDevice(0)

# Boot the server
s.boot()

# Start the server
s.start()

noise = Noise()

# Use a low-pass filter with noise as input
filt = ButLP(noise)  # Stereo output

lfo = Sine(freq=0.1, mul=100, add=500)
filt.freq = lfo

# Reverb for spatial effect
rev = Freeverb(filt)  # Stereo output


# Create a stereo mixer with 2 channels (left and right)
mixer = Mixer(outs=2)

# Add the sine wave to both the left (0) and right (1) channels of the mixer
mixer.addInput(0, filt)
mixer.setAmp(0, 0, 1)  # Channel 0 input to left output
mixer.setAmp(0, 1, 1)  # Channel 0 input to right output

# Output the mixed audio
mixer.out()

# The script will keep running, and the sine wave will play indefinitely
while True:
    pass
