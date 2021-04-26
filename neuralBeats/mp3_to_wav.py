import subprocess
import os

def main(playlist, song_name):
    # files
    src = os.getcwd() + "/" + song_name + ".mp3"
    dst = song_name + ".wav"

    # convert mp3 to wav file
    subprocess.call(['ffmpeg', '-i', src,
                 dst])
