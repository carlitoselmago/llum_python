import numpy as np
import sounddevice as sd
from scipy.signal import butter, filtfilt

def generate_wind_chunk(chunk_length, sample_rate, seed):
    np.random.seed(seed)
    # Generate white noise for the chunk
    noise = np.random.normal(0, 1, int(sample_rate * chunk_length))

    # Design a filter to mimic wind characteristics
    b, a = butter(N=1, Wn=0.1, btype='low')
    wind_chunk = filtfilt(b, a, noise)

    # Normalize to float32 range
    wind_chunk_normalized = np.float32(wind_chunk / np.max(np.abs(wind_chunk)))

    return wind_chunk_normalized

def callback(outdata, frames, time, status):
    global seed
    if status:
        print(status, file=sys.stderr)
    chunk = generate_wind_chunk(chunk_length, sample_rate, seed)
    outdata[:] = chunk.reshape(-1, 1)
    seed += 1  # Update seed for the next chunk

# Parameters
chunk_length = 0.5  # seconds for each chunk
sample_rate = 44100  # Hz
seed = 123  # Custom seed

# Stream setup
stream = sd.OutputStream(
    channels=1,
    samplerate=sample_rate,
    callback=callback
)

# Start streaming
with stream:
    input("Press Enter to stop the wind sound...")

print("Wind sound stopped.")
