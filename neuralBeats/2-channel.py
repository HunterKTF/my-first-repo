import math
import numpy as np
import wave

# Open the wav file from directory
file = wave.open('st1.wav', 'rb')

# Get the file properties
channels = file.getnchannels()
frame_r = file.getframerate()
samp_width = file.getsampwidth()
frames = file.getnframes()

# Reading frame data
data = file.readframes(frames)
wav_data = np.frombuffer(data, 'int16')
data_n = np.int16((wav_data / wav_data.max()) * 32767)

# Making indexing arrays
L = np.arange(0,data_n.size,2)
R = np.arange(1,data_n.size,2)

wav_data_left = data_n[L]
wav_data_right = data_n[R]

from scipy.io.wavfile import write
write("clean1.wav", frame_r, wav_data_left)
write("clean2.wav", frame_r, wav_data_right)

from pydub import AudioSegment

left_channel = AudioSegment.from_wav("clean1.wav")
right_channel = AudioSegment.from_wav("clean2.wav")

stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
