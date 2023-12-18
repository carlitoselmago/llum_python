#https://github.com/audiolabs/SC-Wind-Noise-Generator/blob/main/sc_wind_noise_generator.py
import numpy as np
from sc_wind_noise_generator import WindNoiseGenerator as wng
import sounddevice as sd
import threading
import time

import time

# Include the provided WindNoiseGenerator class here
# ...

FS=48000  # Sample frequency in Hz
DURATION=10 #duration in seconds

class ContinuousWindNoiseGenerator(wng):
    def __init__(self, shared_params, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.shared_params = shared_params
        self.current_position = 0
        self.wind_noise, self.wind_profile = self.generate_wind_noise()

    def generate_continuous_chunk(self, frames):
        # Check if wind_noise is generated
        if not hasattr(self, 'wind_noise'):
            self.wind_noise, self.wind_profile = self.generate_wind_noise()

        # Check for updated parameters
        self._update_params()

        # Generate a chunk of the wind noise
        if self.current_position + frames > len(self.wind_noise):
            self.current_position = 0

        chunk = self.wind_noise[self.current_position:self.current_position + frames]
        self.current_position += frames

        return chunk

    def _update_params(self):
        # Update the wind noise generator parameters if they have changed
        if self.shared_params['update']:
            self.gustiness = self.shared_params['gustiness']
            self.wind_profile = self.shared_params['wind_profile']
            self.wind_noise, self.wind_profile = self.generate_wind_noise()
            self.shared_params['update'] = False

def update_params_thread(shared_params):
    while True:
        # Here you can add your logic to change the parameters
        # For example, you could listen to user input or generate random values
        #time.sleep(5)  # Update every 5 seconds for demonstration
        time.sleep(0.5)
        shared_params['gustiness'] = np.random.randint(4, 20)
        shared_params['wind_profile'] = np.random.uniform(3, 7, size=15)
        shared_params['update'] = True

def callback(outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    chunk = wn_generator.generate_continuous_chunk(frames)
    outdata[:] = chunk.reshape(-1, 1)

# Shared parameters
shared_params = {
    'gustiness': 10,
    'wind_profile': np.array([3.45, 6.74, 5.65, 6.34, 4.00, 5.88, 3.26, 3.19, 4.78, 4.16, 4.67, 4.69, 4.61, 6.53, 6.05]),
    'update': False
}

# Initialize the WindNoiseGenerator with shared parameters
wn_generator = ContinuousWindNoiseGenerator(shared_params, fs=FS, duration=DURATION)

# Start a thread to update parameters
param_update_thread = threading.Thread(target=update_params_thread, args=(shared_params,))
param_update_thread.start()

# Stream setup
stream = sd.OutputStream(
    channels=1,
    samplerate=FS,
    callback=callback,
    blocksize=int(FS * 0.5)  # Adjust block size for smaller audio blocks
)

# Start streaming
with stream:
    input("Press Enter to stop the wind sound...")

print("Wind sound stopped.")
