from pyo import *
import time
import random
import numpy as np
from time import sleep
import sys

class Sound:

    def __init__(self,dmxosc,audiodeviceindex=0):
        self.dmxosc=dmxosc
        self.audiodeviceindex=audiodeviceindex
        pass


    def start(self):
        s = Server(audio="jack")#Server(sr=44100, buffersize=4056)
        sleep(5)
        pa_list_devices()
        s.setInOutDevice(self.audiodeviceindex)  # Make sure this device supports stereo
        s.boot()
        
        
        s.start()
        #pa_list_devices()

        #pitches = [midiToHz(m) for m in [36, 43, 48, 55, 60, 62, 64, 65, 67, 69, 71, 72]]

        # Create a white noise generator
        noise = Noise()

        # Use a low-pass filter with noise as input
        filt = ButLP(noise)  # Stereo output

        # LFO to modulate filter frequency
        lfo = Sine(freq=0.1, mul=100, add=500)
        filt.freq = lfo

        # Reverb for spatial effect
        rev = Freeverb(filt)  # Stereo output

        # Create a stereo mixer with 2 channels (left and right)
        mixer = Mixer(outs=2)

        # Add the noise to both the left (0) and right (1) channels of the mixer
        mixer.addInput(0, filt)
        mixer.setAmp(0, 0, 1)  # Channel 0 input to left output
        mixer.setAmp(0, 1, 1)  # Channel 0 input to right output

        # Output the mixed audio
        mixer.out()

        while True:
            filt.freq=self.dmxosc.scale_single_value(self.dmxosc.dmxdata[10],255,0,200,1800)
            #lfo.freq=self.dmxosc.scale_single_value(self.dmxosc.dmxdata[10],255,0,0.1,2)
            pass
        print("ENDDDD")
        sys.exit()