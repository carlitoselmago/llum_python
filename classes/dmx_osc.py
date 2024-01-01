from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
from classes.pyo import Sound
import numpy as np
import threading
import sys
import time

class dmx_osc:

    oscport = 54321
    rangetime=15 #iterations it takes to define the margin of static sensors
    dmxspeed=0.0001 #speed in seconds for the dmx loop (the lower the faster)
    decay_rate = 0.000000000001
    movement_threshold=0 # value difference for dinamic sensors


    ###################

    sensors=[]
    fixtures=[]
    pairs={}

    dmxport=""
    margin_padding=0.2

    osc_channel=2

    margins={}

    sensor_val={}
    sensor_last_amount=5
    sensor_last_vals={}

    dmxdata={}
    dmxchannel_data_chain={}


    def __init__(self,oscport=54321,rangetime=25,audiodeviceindex=0,dmxport="",device_type="",margin_padding=0,sensors=[],fixtures=[],pairs={}):
        self.oscport=oscport
        self.rangetime=rangetime
        self.dmxport=dmxport
        self.device_type=device_type
        self.margin_padding=margin_padding

        self.sensors=sensors
        self.fixtures=fixtures 
        self.pairs=pairs 

        self.dmx = pyDMXController(port=self.dmxport, device_type=self.device_type)

        self.prepareData()

        self.startOSC()

        
        dmx_thread = threading.Thread(target=self.sendDMXLoop)
        dmx_thread.start()

        self.Sound=Sound(self,audiodeviceindex)
        sound_thread = threading.Thread(target=self.Sound.start)
        sound_thread.start()

    def prepareData(self):
        for s in self.sensors:
            if s["type"]=="static":
                self.margins[s["id"]]={"min":200.0,"max":-200.0,"tested":0}
        
        #prepare dmx array
        for id in self.fixtures:
            for c in self.fixtures[id]["channels"]:
                self.dmxdata[c]=255
              
        for sensorid in self.pairs:
            pair=self.pairs[sensorid]
            for fixture in pair:
                for dmxchannel in self.fixtures[fixture["fixture"]]["channels"]:
                    if dmxchannel not in self.dmxchannel_data_chain:
                        self.dmxchannel_data_chain[dmxchannel]=[]
                    self.dmxchannel_data_chain[dmxchannel].append({"sensorid":sensorid,"type":self.getSensorType(sensorid)})
                    self.sensor_val[sensorid]=255
                    self.sensor_last_vals[sensorid]=[255]*self.sensor_last_amount
        
        print("CREATED dmxchannel_data_chain (DMXchannel-> order of sensors): ")
        print(self.dmxchannel_data_chain)
        print("")
        

    def startOSC(self):
        # Setting up the OSC dispatcher
        disp = dispatcher.Dispatcher()
        for s in self.sensors:
            disp.map("/board" + str(s["id"]), self.senseLoop)

        # Setting up the OSC server
        server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", self.oscport), disp)
        print("Serving on {}".format(server.server_address))

        # Function to run the server
        def run_server():
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                print("Server stopped by user")
            finally:
                server.server_close()

        # Running the OSC server in a separate thread
        server_thread = threading.Thread(target=run_server)
        server_thread.start()

    def senseLoop(self,adress, *args):
        # Handle sensor data here
        #print("Sensor ", adress, "Args:", args)
        sensorid=int(adress[-1])
        value=list(args)[self.osc_channel]
        
        if sensorid in self.margins:
            #static sensors
            if self.margins[sensorid]["tested"]<self.rangetime:
                #print("defining limits of sensor",sensorid)
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
            else:
                #save the data
                if sensorid in self.pairs:
                    for pair in self.pairs[sensorid]:
                        #scale data
                        dmxrange=pair["range"]
                        pvalue=self.scale_single_value(value,self.margins[sensorid]["min"],self.margins[sensorid]["max"],dmxrange[0],dmxrange[1])
                        pvalue=abs(255-pvalue)
                        self.sensor_val[sensorid]=pvalue
                        """
                        if pair["fixture"] in self.fixtures:
                            for chan in self.fixtures[pair["fixture"]]["channels"]:
                                
                                final_value=abs(255-pvalue)
                                #print(final_value)
                                self.dmxdata[chan]=255-final_value#self.lerp(self.dmxdata[chan],pvalue,0.8)
                                #print(self.dmxdata[chan])
                                #print(self.dmxdata[chan])
                        """     
                             
                        
        else:
            # Dynamic sensors
            if sensorid in self.pairs:
                for pair in self.pairs[sensorid]:
                    dmxrange = pair["range"]
                    current_time = time.time()
                    for chan in self.fixtures[pair["fixture"]]["channels"]:
                        #print(value)
                        pvalue = abs(value)  # in a range from 0 to 50 approx
                        pvalue=self.scale_single_value(pvalue, 0, 10, dmxrange[1], dmxrange[0])
                        self.sensor_last_vals[sensorid].append(self.sensor_val[sensorid])
                        if len(self.sensor_last_vals[sensorid])>self.sensor_last_amount:
                            self.sensor_last_vals[sensorid].pop(0)
                        self.sensor_val[sensorid]=pvalue
                        #print(self.sensor_last_vals[sensorid])
                        """
                        if sensorid in self.sensor_last:
                            if (pvalue + self.sensor_last[sensorid]['value']) > self.movement_threshold:
                                time_elapsed = current_time - self.sensor_last[sensorid]['time']
                                decay_amount = self.decay_rate#self.decay_rate * time_elapsed  # Decay depends on elapsed time
                                pvalue = max(pvalue - decay_amount, 0)  # Ensure pvalue doesn't go below 0
                                print(pvalue, "decay", decay_amount)

                                final_value = self.scale_single_value(pvalue, 0, 10, dmxrange[0], dmxrange[1])
                                self.dmxdata[chan] = final_value
                            else:
                                # Handle cases where there's not enough movement
                                pass
                        self.sensor_last[sensorid] = {'value': pvalue, 'time': current_time}
                        """
                            
           

    def sendDMXLoop(self):

        self.dmx.update_channel(6,255) ### THIS IS ONLY FOR LOCAL TEST

        while True:
            for chan in self.dmxchannel_data_chain:
                alpha = 0.2  # Smoothing factor, you can adjust this between 0 and 1
                value = 255
                #TODO: improve this, maybe return to the idea of discounting over time
                for sensor in self.dmxchannel_data_chain[chan]:
                    if sensor["sensorid"] in self.sensor_val:
                        if sensor["type"] == "dinamic":
                            smooth_value=float(np.average(self.sensor_last_vals[sensor["sensorid"]]))
                            #smooth_value=self.sensor_val[sensor["sensorid"]]
                            #if self.sensor_val[sensor["sensorid"]]<self.sensor_last_val[sensor["sensorid"]]:
                            #    smooth_value=self.sensor_last_val[sensor["sensorid"]]-0.1
                            # Exponential smoothing
                            #smooth_value = alpha * self.sensor_val[sensor["sensorid"]] + (1 - alpha) * self.sensor_last_val[sensor["sensorid"]]
                            #print(smooth_value, value, self.sensor_val[sensor["sensorid"]], self.sensor_last_val[sensor["sensorid"]])
                            #value -= smooth_value
                            value-= smooth_value
                            
                        else:
                            value -= self.sensor_val[sensor["sensorid"]]
                self.dmxdata[chan]=value
                self.dmx.update_channel(chan, max(min(int(value), 255), 0))
            """

            for chan in self.dmxdata:
                self.dmx.update_channel(chan, max(min(int(self.dmxdata[chan]),255),0) )
                #if chan==8:
                #    print(int(self.dmxdata[chan]))
            self.dmx.run(self.dmxspeed)
            """
            self.dmx.run(self.dmxspeed)

    def putDatainChain(self):
        pass

    ## HELPER FUNCTIONS

    def getSensorType(self,sensorid):
        for sensor in self.sensors:
            if sensor["id"]==sensorid:
                return sensor["type"]
            
    def lerp(self,start, end, t):
        """
        Linear interpolation between start and end.
        t: interpolation factor (0.0 to 1.0)
        """
        return start + t * (end - start)
            
    def ease_in_quad(self,start, end, t):
        """
        Quadratic easing in: accelerating from zero velocity.
        """
        return start + (end - start) * t * t
    
    def scale_single_value(self,value, old_min, old_max, new_min, new_max):
        """
        Scale a single float value from one range to another, allowing for inverted scales.

        Parameters:
        value (float): The float value to be scaled.
        old_min (float): The minimum value of the original range.
        old_max (float): The maximum value of the original range.
        new_min (float): The minimum value of the new range.
        new_max (float): The maximum value of the new range.

        Returns:
        float: The scaled value.
        """
        # Handle special case where the old range or new range is zero
        if old_max == old_min:
            return new_min

        # Calculate the scale factor and scaled value
        scale = (new_max - new_min) / (old_max - old_min)
        scaled_value = new_min + (value - old_min) * scale

        # Clamping the result within the new range
        return min(max(scaled_value, min(new_min, new_max)), max(new_min, new_max))
