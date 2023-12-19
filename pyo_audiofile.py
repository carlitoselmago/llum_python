from pyo import *

# Initialize the pyo server
s = Server()
s.setInOutDevice(12)
pa_list_devices()
s.boot()
# Load the audio file
snd = SfPlayer("wind_noise.wav", speed=1, loop=True)

# Apply a reverb effect
rev = STRev(snd, inpos=0.5, revtime=1.5, cutoff=5000, bal=0.3).out()

# Apply a delay effect
dly = Delay(snd, delay=0.5, feedback=0.5).out()

# Start the server
s.start()

# Use this to keep the script running
s.gui(locals())
