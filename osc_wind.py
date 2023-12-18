import matplotlib.pyplot as plt
from pythonosc import dispatcher, osc_server
import threading
import numpy as np

def interpolate(start, end, steps):
    return np.linspace(start, end, steps)

# Global variables
values = [0.0]
running = True

#synth
from pyo import *
import time
import random

s = Server(sr=44100, buffersize=4056,nchnls=2)
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

s.start()

# Function to handle incoming OSC messages on /board0
def handle_board0(unused_addr, *args):
    global values
    if len(args) == 1 and all(isinstance(arg, float) for arg in args):
        values = list(args)
        #print(f"Received values: {values}")
    else:
        print(f"Invalid message format: {args}")

# Setting up the OSC server
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/board0", handle_board0)

server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", 54321), dispatcher)
print("Serving on {}".format(server.server_address))

# Function to update the plot
def live_plotter():
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.2)
    
    # Set y-axis limits here (min, max)
    ax.set_ylim([0, 100])  

    # Button click event handler
    def on_close(event):
        global running
        running = False

    fig.canvas.mpl_connect('close_event', on_close)

    current_freq = 500  # Starting frequency
    rate_of_change = 5  # Change in frequency per iteration

    while running:
        
        #synth modification :::::::::::::::::::::::::::::::::::::::::::::::::::::::::
        
        target_freq = values[0] * 200 + 500
        # Update current_freq towards target_freq in small steps
        if current_freq < target_freq:
            current_freq = min(current_freq + rate_of_change, target_freq)
        elif current_freq > target_freq:
            current_freq = max(current_freq - rate_of_change, target_freq)

        filt.freq = current_freq  # Update the filter frequency

        #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::


        #plt.pause(0.2)
        ax.clear()
        ax.bar(['Value1'], values)
        ax.set_ylim([0, 5])  # Maintain y-axis limits after clearing the axes
        plt.draw()

    plt.close(fig)

# Running the OSC server in a separate thread
server_thread = threading.Thread(target=server.serve_forever)
server_thread.start()

# Running the plotter in the main thread
live_plotter()

# After closing the plot window
server.shutdown()
server_thread.join()
print("Server and plot closed.")
s.stop()