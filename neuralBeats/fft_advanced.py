import math
import numpy as np
import wave
import matplotlib.pyplot as plt

# Open the wav file from directory
file = wave.open('st1.wav', 'rb')


# Get the file properties
channels = file.getnchannels()
frame_r = file.getframerate()
samp_width = file.getsampwidth()
frames = file.getnframes()
# file.close()

# Get the file time in minutes
# file_duration = (frames / frame_r) / 60
# frac, num = math.modf(file_duration)
# print("file duration: ", int(num), ":", int(frac*60))

# Make N dimension array for wav_data
N = np.arange(1,frames+1)

# Reading frame data
data = file.readframes(frames)
wav_data = np.frombuffer(data, 'int16')
data_n = np.int16((wav_data / wav_data.max()) * 32767)
print("Total Wave Data array size: ", data_n.size)

# Making indexing arrays
L = np.arange(0,data_n.size,2)
R = np.arange(1,data_n.size,2)

wav_data_left = data_n[L]
wav_data_right = data_n[R]

# Rewind wav file
file.rewind()

# Tell current position
print("Reset file position to: ", file.tell())


# Plot data file
# plt.plot(N, wav_data_left)
# plt.show()

# FFT function
from scipy.fft import rfft, rfftfreq

# Number of samples in normalized_tone
yf = rfft(wav_data_left)
xf = rfftfreq(N.size, 1 / frame_r)

# plt.plot(xf, np.abs(yf))
# plt.show()

# Applying filtering
points_per_frequency = len(xf) / (frame_r / 2)
target_idx1 = int(points_per_frequency * 150)
target_idx2 = int(points_per_frequency * 500)
target_idx3 = int(points_per_frequency * 800)
target_idx4 = int(points_per_frequency * 1200)
target_idx5 = int(points_per_frequency * 1600)
target_idx6 = int(points_per_frequency * 2000)

eq_bandwidth = int(points_per_frequency * 100)

band1 = yf[target_idx1 - eq_bandwidth : target_idx1 + eq_bandwidth]
band2 = yf[target_idx2 - eq_bandwidth : target_idx2 + eq_bandwidth]
band3 = yf[target_idx3 - eq_bandwidth : target_idx3 + eq_bandwidth]
band4 = yf[target_idx4 - eq_bandwidth : target_idx4 + eq_bandwidth]
band5 = yf[target_idx5 - eq_bandwidth : target_idx5 + eq_bandwidth]
band6 = yf[target_idx6 - eq_bandwidth : target_idx6 + eq_bandwidth]

mean1 = np.mean(band1)
dif_arr = band1 - mean1
add_arr = band1 * dif_arr * -1.5
band1 = band1 + add_arr

mean2 = np.mean(band2)
dif_arr = band2 - mean2
add_arr = band2 * dif_arr * -1.9
band2 = band2 + add_arr

mean3 = np.mean(band3)
dif_arr = band3 - mean3
add_arr = band3 * dif_arr * 1.0
band3 = band3 + add_arr

mean4 = np.mean(band4)
dif_arr = band4 - mean4
add_arr = band4 * dif_arr * 1.2
band4 = band4 + add_arr

mean5 = np.mean(band5)
dif_arr = band5 - mean5
add_arr = band5 * dif_arr * 1.5
band5 = band5 + add_arr

mean6 = np.mean(band6)
dif_arr = band6 - mean6
add_arr = band6 * dif_arr * 1.4
band6 = band6 + add_arr

# plt.plot(xf, np.abs(yf))
# plt.show()

# Applyinng reverse function
from scipy.fft import irfft

new_sig = irfft(yf)

# plt.plot(new_sig[:1000])
# plt.show()

# Creating new file
wav_data_left = np.int16(new_sig * (32767 / new_sig.max())) # * (32767 / new_sig.max())

from scipy.io.wavfile import write
write("clean1.wav", frame_r, wav_data_left)
write("clean2.wav", frame_r, wav_data_right)

from pydub import AudioSegment

left_channel = AudioSegment.from_wav("clean1.wav")
right_channel = AudioSegment.from_wav("clean2.wav")

stereo_sound = AudioSegment.from_mono_audiosegments(left_channel, right_channel)
file_handle = stereo_sound.export("out1.wav", format="wav")
