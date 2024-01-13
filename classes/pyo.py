from pyo import *
import time
import random
import numpy as np
from time import sleep
import sys
import threading

class Sound:

    controllers=4
    oldamount=80
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
        s = Server(audio="jack",sr=44100, buffersize=96000)#Server(sr=44100, buffersize=4056)
        sleep(5)
        pa_list_devices()
        s.setInOutDevice(self.audiodeviceindex)  # Make sure this device supports stereo
        s.boot()
        
        #synth part
        s.start()
        #pa_list_devices()
        """
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
        """
        #####################################################################

        # Load audio files
        audio1 = SfPlayer("audio1.wav", loop=True)
        audio2 = SfPlayer("audio2.wav", loop=True).out()
        """
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
        #filt = ButBP(audio1, freq=100, q=5).out()
        freq = Sig(1000)
        freq.ctrl([SLMap(50, 5000, "lin", "value", 1000)], title="Cutoff Frequency")

        # Three different lowpass filters
        tone = Tone(, freq)
        butlp = ButLP(n, freq)
        mooglp = MoogLP(n, freq)

        # Interpolates between input objects to produce a single output
        sel = Selector([tone, butlp, mooglp]).out()
        """

        # Common cutoff frequency control
        freq = Sig(1000)
        #freq.ctrl([SLMap(50, 5000, "lin", "value", 1000)], title="Cutoff Frequency")
        n=audio1
        # Three different lowpass filters
        tone = Tone(n, freq)
        butlp = ButLP(n, freq)
        mooglp = MoogLP(n, freq)

        # Interpolates between input objects to produce a single output
        sel = Selector([tone, butlp, mooglp])#.out()
        #sel.ctrl(title="Filter selector (0=Tone, 1=ButLP, 2=MoogLP)")
        
        rev = Freeverb(sel, size=1, damp=0.7, bal=0.5).out()

        # Volume control
        #vol1 = SigTo(value=0.5, time=0.1, init=0.5)
        #vol2 = SigTo(value=0.5, time=0.1, init=0.5)
        #audio1.mul = vol1
        #audio2.mul = vol2
           
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
                #print(sensor_data)
                for index in sensor_data:
                    

                    sensor_val=sensor_data[index]
                    self.putData(index,sensor_val)
                  
                    if index==0:
                        val=self.getData(index)
                        freq.value=val
                        #all2.feedback=sensor_val#self.getData(index)
                        #filt.freq=self.getData(index)
                        pass
                   
                    if index==1:
                        audio1.mul=self.getData(index)
                        #print(val)
                        #filt.freq=sensor_val#self.getData(index)
                        
                        #all2.feedback=self.getData(index)#random.uniform(0.1,1)
                        pass 
                    
                    if index==2:
                        val=self.getData(index)  
                        #print(val)
                        audio2.mul=val
                        #vol1.value=sensor_val#self.getData(index)
                        #vol1.value = self.getData(index)#random.uniform(0.9, 1)
                        pass 

                    if index==3:
                        val=self.getData(index) 
                        print(val)
                        rev.bal=val
                    """
                    if index==3:
                        pass
                    """
                #dmx_data = self.queue.get()
                #print(dmx_data)
                #filt.freq=self.dmxosc.scale_single_value(dmx_data,-50,50,400,1800)
                
            #sleep(0.0001)
            pass
        print("ENDDDD")
        sys.exit()

    