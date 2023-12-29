from pythonosc import dispatcher, osc_server
from pyDMXController import pyDMXController
import threading

# Settings
port = 54321
channel=2
rangetime=15 #iterations it takes to define the margin of static sensors
margin_padding=0.2

# Sensors
sensors = [
    {"type":"static","id":7}
]

#fixtures
fixtures=[
    {id:0,"channels":[7,8,9],"type":"new"} #test
]

# pairs of sensors and fixtures
pairs={
    7:[0]
}

#################################################################################

#margins
margins={}

"""
dmx = DMXConnection('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0')

dmx.dmx_frame[6] = 255
dmx.dmx_frame[7] = 255
dmx.render()
"""

dmx =  pyDMXController(port='/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A50285BI-if00-port0', device_type='ftdi')
dmx.update_channel(6, 255)  # Set channel 6 to maximum
dmx.update_channel(7, 255)  
dmx.run(5)



for s in sensors:
    if s["type"]=="static":
        margins[s["id"]]={"min":200.0,"max":-200.0,"tested":0}

# Function to handle incoming OSC messages on /board0
def handle_board(adress, *args):
    # Handle sensor data here
    #print("Sensor ", adress, "Args:", args)
    sensorid=int(adress[-1])
    value=list(args)[channel]

    if sensorid in margins:
        if margins[sensorid]["tested"]<rangetime:
            print("defining limits of sensor",sensorid)
            if value<margins[sensorid]["min"]:
                margins[sensorid]["min"]=value
            if value>margins[sensorid]["max"]:
                margins[sensorid]["max"]=value
            margins[sensorid]["tested"]+=1
        elif margins[sensorid]["tested"]==rangetime:
            margins[sensorid]["min"]=margins[sensorid]["min"]-margin_padding
            margins[sensorid]["max"]=margins[sensorid]["max"]+margin_padding
            margins[sensorid]["tested"]+=1
            print("margins set for sensor",sensorid,margins[sensorid])
        
    

# Setting up the OSC dispatcher
disp = dispatcher.Dispatcher()
for s in sensors:
    disp.map("/board" + str(s["id"]), handle_board)

# Setting up the OSC server
server = osc_server.ThreadingOSCUDPServer(("0.0.0.0", port), disp)
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
