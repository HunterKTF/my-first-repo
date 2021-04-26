import numpy as np
import wave
import matplotlib.pyplot as plt
import os
from os import path
from pydub import AudioSegment
import spotify_to_mp3
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
from scipy.io.wavfile import write
import time


def call_spotify():
    # Download the playlist songs
    playlist_name = spotify_to_mp3.main()

    # Import the text file with all the available songs
    songs = []
    current_dir = os.getcwd()
    playlist_file = current_dir + "/" + playlist_name + ".txt"
    file_open = open(playlist_file)
    for song in file_open:
        # Parse song name for conversion to wave file
        song_split = song.split(",")
        song_name = song_split[0]
        spotify_to_mp3.mp3_to_wav(playlist_name, song_name)
        songs.append(song_name)

    # Songs menu
    print("Your songs from the playlist are: ")
    print(songs)

    # Input the name of the song without extension:
    song_name = input("Input the name of the song: ")
    return song_name


def analyze_song(song_name):
    # Open the wav file from directory
    wav_file = song_name + ".wav"
    wav_open = wave.open(wav_file, 'rb')


    # Extracting file properties
    frame_r = wav_open.getframerate()
    frames = wav_open.getnframes()
    channels = wav_open.getnchannels()

    # Reading frame data
    data = wav_open.readframes(frames)
    wav_data = np.frombuffer(data, 'int16')
    data_n = np.int16((wav_data / wav_data.max()) * 32767)

    # Making indexing arrays
    L = np.arange(0,data_n.size,2)
    R = np.arange(1,data_n.size,2)

    wav_data_left = data_n[L]
    wav_data_right = data_n[R]

    # Make N dimension array for wav_data
    N = np.arange(1,frames+1)

    # Plot data file
    # plt.plot(N, wav_data_left)
    # plt.show()

    '''
    Left Ear EQ
    '''
    # Number of samples in normalized_tone
    yfL1 = rfft(wav_data_left)
    yfR1 = rfft(wav_data_right)
    xf = rfftfreq(N.size, 1 / frame_r)

    # plt.plot(xf, np.abs(yf))
    # plt.show()

    # Applying filtering
    points_per_frequency = len(xf) / (frame_r / 2)
    eq_bandwidth = int(points_per_frequency * 5)
    for x in range(1,13):
        target_idx = int(points_per_frequency * (x+1) * 200)
        band = yfL1[target_idx - eq_bandwidth : target_idx + eq_bandwidth]
        band += 10000
        # diff_arr = band - np.mean(band)
        # band += -band*diff_arr
        yfL1[target_idx - eq_bandwidth : target_idx + eq_bandwidth] = band

    for x in range(1,13):
        target_idx = int(points_per_frequency * (x+1) * 300)
        band = yfR1[target_idx - eq_bandwidth : target_idx + eq_bandwidth]
        band -= 10000
        # diff_arr = band - np.mean(band)
        # band += -band*diff_arr
        yfR1[target_idx - eq_bandwidth : target_idx + eq_bandwidth] = band


    # Multi channel
    yfL2 = rfft(wav_data_left)
    yfR2 = rfft(wav_data_right)
    for x in range(1,13):
        target_idx = int(points_per_frequency * (x+1) * 200)
        band = yfL1[target_idx - eq_bandwidth : target_idx + eq_bandwidth]
        band += 20000
        # diff_arr = band - np.mean(band)
        # band += -band*diff_arr
        yfL1[target_idx - eq_bandwidth : target_idx + eq_bandwidth] = band

    for x in range(1,13):
        target_idx = int(points_per_frequency * (x+1) * 300)
        band = yfR1[target_idx - eq_bandwidth : target_idx + eq_bandwidth]
        band -= 20000
        # diff_arr = band - np.mean(band)
        # band += -band*diff_arr
        yfR1[target_idx - eq_bandwidth : target_idx + eq_bandwidth] = band


    # plt.plot(xf, np.abs(yf))
    # plt.show()

    # Get the inverse of function yf
    sigL1 = irfft(yfL1)
    sigR1 = irfft(yfR1)
    sigL2 = irfft(yfL2)
    sigR2 = irfft(yfR2)

    # plt.plot(sigL)
    # plt.show()

    # Creating new file
    wav_data_left1 = np.int16(sigL1 * (32767 / sigL1.max()))
    wav_data_right1 = np.int16(sigR1 * (32767 / sigR1.max()))
    wav_data_left2 = np.int16(sigL2 * (32767 / sigL2.max()))
    wav_data_right2 = np.int16(sigR2 * (32767 / sigR2.max()))

    write("EQL1.wav", frame_r, wav_data_left)
    write("EQR1.wav", frame_r, wav_data_right)
    write("EQL2.wav", frame_r, wav_data_left)
    write("EQR2.wav", frame_r, wav_data_right)

    left_channel1 = AudioSegment.from_wav("EQL1.wav")
    right_channel1 = AudioSegment.from_wav("EQR1.wav")
    left_channel2 = AudioSegment.from_wav("EQL2.wav")
    right_channel2 = AudioSegment.from_wav("EQR2.wav")

    stereo_sound = AudioSegment.from_mono_audiosegments(left_channel1, right_channel1, left_channel2, right_channel2)
    file_handle = stereo_sound.export("EQFinal.wav", format="wav")


if __name__ == "__main__":
    # song_name = call_spotify()
    start_time = time.time()
    song_name = "Test/Rise Up"
    analyze_song(song_name)
    print("--- %s seconds ---" % (time.time() - start_time))
