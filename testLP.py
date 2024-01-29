from pyo import *

s = Server(audio="jack",sr=44100, buffersize=96000).boot()

# White noise generator
n = Noise(0.5)

# Common cutoff frequency control
freq = Sig(1000)
freq.ctrl([SLMap(50, 5000, "lin", "value", 1000)], title="Cutoff Frequency")

# Three different lowpass filters
tone = Tone(n, freq)
butlp = ButLP(n, freq)
mooglp = MoogLP(n, freq)

# Interpolates between input objects to produce a single output
sel = Selector([tone, butlp, mooglp]).out()
sel.ctrl(title="Filter selector (0=Tone, 1=ButLP, 2=MoogLP)")

# Displays the spectrum contents of the chosen source
sp = Spectrum(sel)

s.gui(locals())