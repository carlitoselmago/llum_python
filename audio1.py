from pyo import *
import random
import time

# Initialize Pyo server
s = Server(audio="jack",sr=44100, buffersize=4056).boot()

s.setInOutDevice(3)

# Load audio files
audio1 = SfPlayer('audio1.mp3', loop=True)
audio2 = SfPlayer('audio2.mp3', loop=True)

# Reverb 1 ##############################################################
#rev = Freeverb(audio1, size=0.8, damp=0.7, bal=0.5).out()

# reverb alternative ####################################################
# Four parallel stereo comb filters. The delay times are chosen
# to be as uncorrelated as possible. Prime numbers are a good
# choice for delay lengths in samples.
comb1 = Delay(audio1, delay=[0.0297, 0.0277], feedback=0.65)
comb2 = Delay(audio1, delay=[0.0371, 0.0393], feedback=0.51)
comb3 = Delay(audio1, delay=[0.0411, 0.0409], feedback=0.5)
comb4 = Delay(audio1, delay=[0.0137, 0.0155], feedback=0.73)

combsum = audio1 + comb1 + comb2 + comb3 + comb4

# The sum of the original signal and the comb filters
# feeds two serial allpass filters.
all1 = Allpass(combsum, delay=[0.005, 0.00507], feedback=0.75)
all2 = Allpass(all1, delay=[0.0117, 0.0123], feedback=0.61)

# Brightness control.
lowp = Tone(all2, freq=3500, mul=0.25).out()

# END reverb 2 ###########################################

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
    #rev.bal = random.uniform(0, 1)
    all2.feedback=random.uniform(0.1,1)

    # Randomize filter frequency
    filt.freq = random.uniform(60, 20000)
    
    # Randomize volumes
    vol1.value = random.uniform(0.9, 1)
    #vol1.value = random.uniform(0.1, 1)
    #vol2.value = random.uniform(0.1, 1)

# Loop to change parameters every 5 seconds
while True:
    randomize()
    time.sleep(5)
