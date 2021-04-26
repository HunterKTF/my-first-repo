import math
import numpy as np
import wave
import matplotlib.pyplot as plt

# Open the wav file from directory
file = wave.open('play2.wav', 'rb')

# Get the file properties
channels = file.getnchannels()
frame_r = file.getframerate()
samp_width = file.getsampwidth()
frames = file.getnframes()

# For testing (seconds)
sec = 3

# Printing wav file attributes
print("no. of channels: ", channels)
print("sampling frequency: ", frame_r)
print("sample width: ", samp_width)
print("no. of frames: ", frames)

# Get the file time in minutes
file_duration = (frames / frame_r) / 60
frac, num = math.modf(file_duration)
print("file duration: ", int(num), ":", int(frac*60))

# Reading frame data
data = file.readframes(1)
wav_data = np.frombuffer(data, 'int16')
wav_data_left = np.array(wav_data[0])
wav_data_right = np.array(wav_data[1])
for x in range(sec*frame_r):
    data = file.readframes(1)
    wav_data_left = np.hstack((wav_data_left, wav_data[0]))
    wav_data_right = np.hstack((wav_data_left, wav_data[1]))

print(wav_data_left.size)
# print(file.tell())

# Rewind wav file
file.rewind()

# Make N dimension array for wav_data
N = np.array([1])
for i in range(1,frame_r*sec):
    N = np.hstack((N, i))

# Plot data file
plt.plot(N, wav_data_left)
plt.show()

# Rewind wav file
file.rewind()

# Tell current position
# print(file.tell())

# FFT function
# from scipy.fft import rfft, rfftfreq

# Number of samples in normalized_tone
# M = frame_r * sec

# yf = rfft(wav_data_left)
# xf = rfftfreq(M, 1 / frame_r)

# plt.plot(xf, np.abs(yf))
# plt.show()
