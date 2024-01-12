from pyo import *
import time
import random
import numpy as np
from time import sleep
import sys

class Sound:

    controllers=4
    oldamount=5
    controldata=[]

    def __init__(self,dmxosc,queue, terminate_flag,audiodeviceindex=0):
        self.queue = queue
        self.terminate_flag = terminate_flag
        self.dmxosc=dmxosc
        self.audiodeviceindex=audiodeviceindex
        self.prepareData()

    def avg(self,lst):
        lst=list(lst)
        return sum(lst) / len(lst) 
    
    def prepareData(self):
        for i in range(self.controllers):
            self.controldata.append([])

    def putData(self,index,value):
        self.controldata[index].append(value)
        if len(self.controldata[index])>self.oldamount:
            self.controldata[index].pop(0)

    def getData(self,index):
        return self.avg(self.controldata[index])

    def start(self):
        s = Server(audio="jack",sr=44100, buffersize=4056)#Server(sr=44100, buffersize=4056)
        sleep(5)
        pa_list_devices()
        s.setInOutDevice(self.audiodeviceindex)  # Make sure this device supports stereo
        s.boot()
        
        #synth part
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
        
        
        #############################################################################

        """
        #set controllers (4 of them)
        controllers={
            0:filt.freq,
            1:lfo.mul,
            2:lfo.add,
           # 3:mixer.amp
        }
        """

        while not self.terminate_flag.value:
            if not self.queue.empty():
                sensor_data=self.queue.get()
                for index in sensor_data:
                    

                    sensor_val=sensor_data[index]
                    self.putData(index,sensor_val)
                    if index==0:
                        filt.freq=self.getData(index)
                
                #dmx_data = self.queue.get()
                #print(dmx_data)
                #filt.freq=self.dmxosc.scale_single_value(dmx_data,-50,50,400,1800)
        
            pass
        print("ENDDDD")
        sys.exit()