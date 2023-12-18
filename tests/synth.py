import numpy as np
import sounddevice as sd
from scipy.signal import butter, filtfilt

def generate_sine_wave(frames, sample_rate, freq):
    t = np.arange(frames) / sample_rate
    return 0.1 * np.sin(2 * np.pi * freq * t)  # Amplitude of sine wave set to 0.1

def generate_wind_chunk(frames, sample_rate, seed, last_chunk_end):
    np.random.seed(seed)
    # Generate white noise for the chunk
    noise = np.random.normal(0, 1, frames)

    # Generate a sine wave with varying frequency for the whistling effect
    freq = np.linspace(300, 600, frames)  # Frequency varies between 300 to 600 Hz
    sine_wave = generate_sine_wave(frames, sample_rate, freq)

    # Combine the sine wave with noise
    combined_signal = noise + sine_wave

    # Design a filter to mimic wind characteristics
    b, a = butter(N=2, Wn=0.05, btype='low')
    wind_chunk = filtfilt(b, a, combined_signal)

    # Blend with the end of the previous chunk for smooth transition
    if last_chunk_end is not None:
        wind_chunk[:1000] = (wind_chunk[:1000] + last_chunk_end) / 2

    # Normalize to float32 range and reduce volume
    wind_chunk_normalized = np.float32(wind_chunk / np.max(np.abs(wind_chunk)) * 0.5)

    return wind_chunk_normalized, wind_chunk[-1000:]

last_chunk_end = None

def callback(outdata, frames, time, status):
    global seed, last_chunk_end
    if status:
        print(status, file=sys.stderr)
    chunk, last_chunk_end = generate_wind_chunk(frames, sample_rate, seed, last_chunk_end)
    outdata[:] = chunk.reshape(-1, 1)
    seed += 1  # Update seed for the next chunk

# Parameters
sample_rate = 244100  # Hz
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
