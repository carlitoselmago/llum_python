from pyo import *
import tkinter

# Initialize the server.
s = Server().boot()

s.setInOutDevice(14)

s.start()

#http://ajaxsoundstudio.com/pyodoc/api/classes/pan.html?highlight=mixer#pyo.Mixer

# Create a simple synthesizer.
synth = Sine(freq=440, mul=0.2)
lfo = Sine(freq=0.1, mul=40, add=440)
synth.freq = lfo
# Create a mixer with 2 channels.
mm = Mixer(outs=2, chnls=2, time=0.025)

# Create a reverb effect.
reverb = Freeverb(mm[0], size=1.0, damp=1, mul=0.5).out()

#delay
delay = Delay(mm[1], delay=0.5, feedback=0.5, mul=0.5).out()

# Add the synthesizer to the first input channel of the mixer.
mm.addInput(0, synth)

# Set the amplitude for sending the signal from channel 0 to the reverb effect.
mm.setAmp(0, 0, 0.1)

def change_amp(channel, output,amp):
    mm.setAmp(channel, output,amp/100)

root = tkinter.Tk()

amp_slider1 = tkinter.Scale(root, from_=0, to=100, orient='horizontal', command=lambda val: change_amp(0,1, float(val)))
amp_slider1.pack()



# Play the synthesizer and the reverb effect.
#synth.out()
mm.out()
# Start the Tkinter event loop
root.mainloop()
s.gui(locals())