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

    def start(self,audioback):
        s = Server(audio=audioback,sr=44100, buffersize=96000)#Server(sr=44100, buffersize=4056)
        sleep(5)
        pa_list_devices()
        s.setInOutDevice(self.audiodeviceindex)  # Make sure this device supports stereo
        s.boot()
        
        #synth part
        s.start()
        #pa_list_devices()
        

        # Load audio files
        audio1 = SfPlayer("audio1.wav", loop=True)
        audio2 = SfPlayer("audio2.wav", loop=True).out()
        
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
                        #print(val)
                        rev.bal=val
                  
              
                
         
            pass
        print("ENDDDD")
        sys.exit()

    