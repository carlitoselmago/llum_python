from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
from classes.pyo import Sound
import numpy as np
import threading
from multiprocessing import Process, Queue, Value
import ctypes
import sys
import time
import random
import logging
logging.disable(logging.DEBUG)

class dmx_osc:

    oscport = 54321
    rangetime=11 #iterations it takes to define the margin of static sensors
    dmxspeed=0.0005 #speed in seconds for the dmx loop (the lower the faster)
    movement_threshold=0 # value difference for dinamic sensors
    sound_enabled=True
    
    endminutes=4 # the time this code should wait till it starts to a fade out
    global_dimmer=1.0

    ###################

    sensors=[]
    fixtures=[]
    pairs={}

    dmxport=""
    margin_padding=0.1

    osc_channels=[3,4,5]

    margins={}

    sensor_val={}
    sensor_last_amount=10
    sensor_last_vals={}

    dmxdata={}
    dmxchannel_data_chain={}
    channeladjustments={}

    sensors_audio_val={}
    sensormin={} #minimum value to be read

    sensor_types={}

    stop_flag = False
    batteries_checked=False

    batterylevel={}

    def __init__(self,oscport=54321,oscip="0.0.0.0",rangetime=25,audiodeviceindex=0,dmxport="",device_type="",margin_padding=0,sensors=[],fixtures=[],pairs={},pairs_audio={},audioback="jack",skip_intro=False,endminutes=15):
        self.oscport=oscport
        self.oscip=oscip
        self.rangetime=rangetime
        self.dmxport=dmxport
        self.device_type=device_type
        self.margin_padding=margin_padding

        self.sensors=sensors
        self.fixtures=fixtures 
        self.pairs=pairs 
        self.pairs_audio=pairs_audio
        self.endminutes=endminutes# the time this code should wait till it starts to a fade out

        if self.sound_enabled: 
            #self.Sound=Sound(self,audiodeviceindex)
            #sound_thread = threading.Thread(target=self.Sound.start)
            #sound_thread.start()
            self.terminate_flag = Value(ctypes.c_bool, False)
            self.sound_queue = Queue(maxsize=2)
            self.Sound = Sound(self,self.sound_queue, self.terminate_flag,audiodeviceindex)
            # Create a process for the sound task
            self.sound_process =Process(target=self.Sound.start,args=(audioback,))
            self.sound_process.start()

        try:
            self.dmx = pyDMXController(port=self.dmxport, device_type=self.device_type)
        except Exception as e:
            print(e)
            self.dmx=False
        self.prepareData()

        self.startOSC()
        if not skip_intro:
            # INIT SEQUENCE ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
            #blackout
            print("blackout ...")
            for c in range(1,200):
                self.dmx.update_channel(c, 0)
                self.dmx.run(self.dmxspeed)
            time.sleep(18)
            #INIT FOG
            print("INIT fog lights...")
            #put RGB to full
            for c in range(62,65):
                value=255
                if c==64:
                    value=255*0.85
                #value=int(255*self.channeladjustments[c])
                #value=255
                self.dmx.update_channel(c, int(value))
            #animate dimmer
            print("init fog...")
            self.dmx.update_channel(60, 255)
            
            self.dmx.run(self.dmxspeed)
            for t in range(1,255):
                self.dmx.update_channel(61, t)
                self.dmx.run(self.dmxspeed)
                time.sleep(0.1)
            #self.dmx.update_channel(61, 255)
            #time.sleep(2)
            
            time.sleep(30)
            print("stop fog...")
            #stop fog
            self.dmx.update_channel(60, 0)
            self.dmx.run(self.dmxspeed)
            time.sleep(15)
            print("pause...")
            for t in reversed(range(1,255)):
                self.dmx.update_channel(61, t)
                self.dmx.run(self.dmxspeed)
                time.sleep(0.08)
            
        else:
            print("::::::::::::::::::::::::")
            print("::::SKIPPING INTRO::::::")
            print("::::::::::::::::::::::::")
        time.sleep(5)
        print("NORMAL START....")
        self.dmx_thread = threading.Thread(target=self.sendDMXLoop)
        self.dmx_thread.start()

        #fadein de dimmer general
        self.global_dimmer=0.0
        for t in range(0,100):
            self.global_dimmer=(t/10.0)
            time.sleep(0.04)

        #end timer thread

        self.end()
        
    def end(self):
        
        def thread_function():
            time.sleep(self.endminutes * 60)
            #END
            print("init fadeout end.....")
            for t in range(1,255):
                self.global_dimmer-=0.01
                if self.global_dimmer<0.1:
                    break
                time.sleep(0.08)
            print("END ::::::::::::::::::::::::::::::::")
            self.stop_flag=True
            

            #stop all threads
            self.server.shutdown()
            self.OSC_thread.join()
            self.dmx_thread.join()
            
           
            #stop audio
            if self.sound_enabled: 
                self.close()
                self.sound_process.terminate()
            sys.exit()
            
        fadeout_thread = threading.Thread(target=thread_function)
        fadeout_thread.start()

    def prepareData(self):
        for s in self.sensors:
            if s["type"]=="static":
                self.margins[s["id"]]={"min":200.0,"max":-200.0,"tested":0}
                print('self.margins[s["id"]]',self.margins[s["id"]])
            
            if "minthreshold" in s:
                self.sensormin[s["id"]]=s["minthreshold"]
            else:
                self.sensormin[s["id"]]=0
            self.sensor_types[s["id"]]=s["type"]
        
        #new fixture white balance for new fixtures
        newWB=[0.34,0.69,0.58,0.27]

        #white balance for fog machine
        fogWB=[1,1,0.9]
               
        
        #prepare dmx array
        for id in self.fixtures:
            if self.fixtures[id]["type"]=="new":
                for i,c in enumerate(self.fixtures[id]["channels"]):
                    #print('newWB[i]',newWB[i])
                    #print(self.channeladjustments)
                    #print('self.channeladjustments[c]',self.channeladjustments[c])
                    try:
                        self.channeladjustments[c]=newWB[i]
                    except:
                        self.channeladjustments[c]=1.0
                    self.dmxdata[c]=0#255
            elif self.fixtures[id]["type"]=="fog":
                for i,c in enumerate(self.fixtures[id]["channels"]):
                    self.channeladjustments[c]=fogWB[i]
            else:
                for c in self.fixtures[id]["channels"]:
                    self.channeladjustments[c]=1.0
                    self.dmxdata[c]=0#255

        for sensorid in self.pairs:
            pair=self.pairs[sensorid]
            #print(pair)
            #print("")
            for fixture in pair:
                #print(self.fixtures[fixture["fixture"]]["channels"])
                #print("+++++++++++++++++++++++++++++++++++++++++++")
                #print("")
                for dmxchannel in self.fixtures[fixture["fixture"]]["channels"]:
                    if dmxchannel not in self.dmxchannel_data_chain:
                        self.dmxchannel_data_chain[dmxchannel]=[]
                    self.dmxchannel_data_chain[dmxchannel].append({"sensorid":sensorid,"type":self.getSensorType(sensorid)})
                    self.sensor_val[sensorid]=0#255
                    self.sensor_last_vals[sensorid]=[0]*self.sensor_last_amount
        
        for sensorid in self.pairs_audio:
            pair=self.pairs_audio[sensorid]
            for controller in pair:
                self.sensors_audio_val[controller["control"]]=self.avg(controller["range"])
                print("audio pair",pair)
                print('self.sensors_audio_val[controller["control"]]',controller["control"],self.sensors_audio_val[controller["control"]])
                print("")

        #print("CREATED dmxchannel_data_chain (DMXchannel-> order of sensors): ")
        #print(self.dmxchannel_data_chain)
        #print("")
        
    

    def startOSC(self):
        # Setting up the OSC dispatcher
        disp = dispatcher.Dispatcher()
        for s in self.sensors:
            disp.map("/board" + str(s["id"]), self.senseLoop)

        # Setting up the OSC server
        self.server = osc_server.ThreadingOSCUDPServer((self.oscip ,self.oscport), disp)
        #server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.oscport), disp)
        print("Serving on {}".format(self.server.server_address))

        # Function to run the server
        def run_server():
            try:
                self.server.serve_forever()
            except KeyboardInterrupt:
                print("Server stopped by user")
            finally:
                print("OSC SERVER CLOSED:::")
                self.server.server_close()

        # Running the OSC server in a separate thread
        self.OSC_thread = threading.Thread(target=run_server)
        self.OSC_thread.start()
        

    def senseLoop(self,adress, *args):
        # Handle sensor data here
        #print("Sensor ", adress, "Args:", args)
        #sensorid=int(adress[-1])
        sensorid=int(adress.split("board")[1])
        #print("sensorid",sensorid)
        rawvalues=list(args)
        if self.sensor_types[sensorid]=="static":
            value=rawvalues[2]
        else:
            if not self.batteries_checked :
                self.batterylevel[sensorid]=rawvalues[6]
            value=np.average(rawvalues[3:5]).item()
            #print(value)
        #print(value,adress)
        #print("self.margins",self.margins)
        #print("sensorid",sensorid)
        if sensorid in self.margins:
            #static sensors
            #print(self.margins[sensorid]["tested"])
            if self.margins[sensorid]["tested"]<self.rangetime:
                if value<self.margins[sensorid]["min"]:
                    self.margins[sensorid]["min"]=value
                if value>self.margins[sensorid]["max"]:
                    self.margins[sensorid]["max"]=value
                self.margins[sensorid]["tested"]+=1
            elif self.margins[sensorid]["tested"]==self.rangetime:
                self.margins[sensorid]["min"]=self.margins[sensorid]["min"]-self.margin_padding
                self.margins[sensorid]["max"]=self.margins[sensorid]["max"]+self.margin_padding
                self.margins[sensorid]["tested"]+=1
                print("margins set for sensor",sensorid,self.margins[sensorid])
                self.batterylevel[sensorid]=rawvalues[6]
               
                    
                if len(self.batterylevel)==len(self.sensors):
                    #print baterry levels
                    print("$$$$$$$$$BATTERY LEVELS$$$$$$$$$$$$$")
                    for bl in self.batterylevel:
                        print("SENSOR "+str(bl),"::",self.batterylevel[bl],"%")
                    print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                    self.batteries_checked=True
                #print("battery ",self.batterylevel[sensorid],"%")
            else:
                #save the data
                if sensorid in self.pairs:
                    for pair in self.pairs[sensorid]:
                        #scale data
                        dmxrange=pair["range"]
                        pvalue=self.scale_single_value(value,self.margins[sensorid]["min"],self.margins[sensorid]["max"],dmxrange[0],dmxrange[1])
                        self.sensor_last_vals[sensorid].append(self.sensor_val[sensorid])
                        pvalue=abs(0+pvalue)
                        self.sensor_val[sensorid]=pvalue
                        
        else:
            # Dynamic sensors
            if sensorid in self.pairs:
                for pair in self.pairs[sensorid]:
                    dmxrange = pair["range"]
                    #current_time = time.time()
                    for chan in self.fixtures[pair["fixture"]]["channels"]:
                        pvalue = abs(value)  # in a range from 0 to 50 approx
                        #pvalue=self.scale_single_value(pvalue, 0, 10, dmxrange[1], dmxrange[0])
                        #print("pvalue",pvalue)
                        if pvalue<self.sensormin[sensorid]:
                            pvalue=0
                        pvalue=self.scale_single_value(pvalue, 0, 10, dmxrange[1], dmxrange[0])
                        self.sensor_last_vals[sensorid].append(self.sensor_val[sensorid])
                        if len(self.sensor_last_vals[sensorid])>self.sensor_last_amount:
                            self.sensor_last_vals[sensorid].pop(0)
                        #print("din s",pvalue)
                        self.sensor_val[sensorid]=pvalue
        #audio pairs
        if sensorid in self.pairs_audio:
            
            for pair in self.pairs_audio[sensorid]:
                dmxrange = pair["range"]
                pvalue = abs(value)
                pvalue=self.scale_single_value(pvalue, 0, 10, dmxrange[1], dmxrange[0])
                #print("audio controller pvalue",pvalue)
                self.sensors_audio_val[pair["control"]]=pvalue

        #time.sleep(0.001)
                       
    def sendDMXLoop(self):

        #self.dmx.update_channel(6,255) ### THIS IS ONLY FOR LOCAL TEST

        while not self.stop_flag:
            for chan in self.dmxchannel_data_chain:
                alpha = 0.2  # Smoothing factor, you can adjust this between 0 and 1
                value = 0 # change this to 255 to make it substractive
                #TODO: improve this, maybe return to the idea of discounting over time
                for sensor in self.dmxchannel_data_chain[chan]:
                    if sensor["sensorid"] in self.sensor_val:
                        if sensor["type"] == "dinamic":
                            smooth_value=float(np.average(self.sensor_last_vals[sensor["sensorid"]]))
                            value+= smooth_value
                        else:
                            #fix for magenta bug on old fixtures
                            if (chan>41 and chan <57):
                                smooth_value=float(np.average(self.sensor_last_vals[sensor["sensorid"]][-3:]))
                                value+= smooth_value
                                #value += self.sensor_val[sensor["sensorid"]]
                            else:
                                smooth_value=float(np.average(self.sensor_last_vals[sensor["sensorid"]][-8:]))
                                value+= smooth_value
                            #print("stattic value",value)
                            #value += self.sensor_val[sensor["sensorid"]]
                #white balance adjustment
                value=value*self.channeladjustments[chan]
                self.dmxdata[chan]=value
                if self.dmx:
                    #print(chan,value)
                    finalvalue=int( max(min(int(value), 255), 0)*self.global_dimmer )
                    #print("finalvalue",finalvalue)

                    #fix for magenta bug on old fixtures
                    if (chan>41 and chan <57):
                        #old ones
                        if finalvalue<25:
                            finalvalue=0   
                    
                    self.dmx.update_channel(chan, finalvalue)
      
            if self.dmx:
                self.dmx.run(self.dmxspeed)
            try:
                if self.sound_enabled: 
                    #print(self.sensors_audio_val)
                    self.sound_queue.put(self.sensors_audio_val)
                    #self.sound_queue.put(self.dmxdata[7])
                pass
               
            except Exception as e:
                print(e)
            #time.sleep(0.001)
        print("END sendDMXLoop::::")

    def close(self):
        self.terminate_flag.value = True
        self.sound_process.terminate()
    
    ## HELPER FUNCTIONS
        
    def avg(self,lst):
        return sum(lst) / len(lst) 

    def getSensorType(self,sensorid):
        for sensor in self.sensors:
            if sensor["id"]==sensorid:
                return sensor["type"]
            
    def lerp(self,start, end, t):
        return start + t * (end - start)
            
    def ease_in_quad(self,start, end, t):
        return start + (end - start) * t * t
    
    def scale_single_value(self,value, old_min, old_max, new_min, new_max):
        # Handle special case where the old range or new range is zero
        if old_max == old_min:
            return new_min

        # Calculate the scale factor and scaled value
        scale = (new_max - new_min) / (old_max - old_min)
        scaled_value = new_min + (value - old_min) * scale

        # Clamping the result within the new range
        return min(max(scaled_value, min(new_min, new_max)), max(new_min, new_max))
