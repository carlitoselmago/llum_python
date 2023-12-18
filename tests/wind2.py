from tests.sc_wind_noise_generator import WindNoiseGenerator as wng

wn = wng(fs=48000)
wn.start_live_playback(chunk_duration=5)  # Start live playback

# The wind noise will now be playing continuously in the background
# Do other things here...

#wn.stop_live_playback()  # Stop live playback when done