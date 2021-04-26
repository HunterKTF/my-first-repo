# Downloads a Spotify playlist into a folder of MP3 tracks
# Jason Chen, 21 June 2020

import os
import subprocess
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.oauth2 as oauth2
import youtube_dl
from youtube_search import YoutubeSearch

# **************PLEASE READ THE README.md FOR USE INSTRUCTIONS**************

def mp3_to_wav(playlist, song_name):
    # files
    src = os.getcwd() + "/" + song_name + ".mp3"
    dst = song_name + ".wav"

    # convert mp3 to wav file
    subprocess.call(['ffmpeg', '-i', src,
                 dst])

def write_tracks(text_file: str, tracks: dict):
    # Writes the information of all tracks in the playlist to a text file. 
    # This includins the name, artist, and spotify URL. Each is delimited by a comma.
    with open(text_file, 'w+', encoding='utf-8') as file_out:
        while True:
            for item in tracks['items']:
                if 'track' in item:
                    track = item['track']
                else:
                    track = item
                try:
                    track_url = track['external_urls']['spotify']
                    track_name = track['name']
                    track_artist = track['artists'][0]['name']
                    csv_line = track_name + "," + track_artist + "," + track_url + "\n"
                    try:
                        file_out.write(csv_line)
                    except UnicodeEncodeError:  # Most likely caused by non-English song names
                        print("Track named {} failed due to an encoding error. This is \
                            most likely due to this song having a non-English name.".format(track_name))
                except KeyError:
                    print(u'Skipping track {0} by {1} (local only?)'.format(
                            track['name'], track['artists'][0]['name']))
            # 1 page = 50 results, check if there are more pages
            if tracks['next']:
                tracks = spotify.next(tracks)
            else:
                break


def write_playlist(username: str, playlist_id: str, sp):
    results = sp.user_playlist(username, playlist_id, fields='tracks,next,name')
    playlist_name = results['name']
    text_file = u'{0}.txt'.format(playlist_name, ok='-_()[]{}')
    print(u'Writing {0} tracks to {1}.'.format(results['tracks']['total'], text_file))
    tracks = results['tracks']
    write_tracks(text_file, tracks)
    return playlist_name


def find_and_download_songs(reference_file: str):
    TOTAL_ATTEMPTS = 10
    with open(reference_file, "r", encoding='utf-8') as file:
        for line in file:
            temp = line.split(",")
            name, artist = temp[0], temp[1]
            text_to_search = artist + " - " + name
            best_url = None
            attempts_left = TOTAL_ATTEMPTS
            while attempts_left > 0:
                try:
                    results_list = YoutubeSearch(text_to_search, max_results=1).to_dict()
                    #print(results_list)
                    format = results_list[-1]
                    best_url = "https://www.youtube.com{}".format(format['url_suffix'])
                    break
                except IndexError:
                    attempts_left -= 1
                    print("No valid URLs found for {}, trying again ({} attempts left).".format(
                        text_to_search, attempts_left))
            if best_url is None:
                print("No valid URLs found for {}, skipping track.".format(text_to_search))
                continue
            # Run you-get to fetch and download the link's audio
            print("Initiating download for {}.".format(text_to_search))
            ydl_opts = {
                'nocheckcertificate': True,
                'format': 'bestaudio/best',
                'outtmpl': name+".mp3",
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([best_url])

def main():
     # Parameters
    username = input("username: ir6jfsd6tp7nmbbzgx8nak2si \n >")
    playlist_uri = input("playlist URI: 6xmIxeqXZtuGBHHi6dEPIC \n >")
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="3848805be43d46d8b092a88d31e83a99",
                                                           client_secret="bd05805564764977a56d3fdfced45ad9"))

    playlist_name = write_playlist(username, playlist_uri, sp)
    reference_file = "{}.txt".format(playlist_name)
    # Create the playlist folder
    if not os.path.exists(playlist_name):
        os.mkdir(playlist_name)
    os.rename(reference_file, playlist_name + "/" + reference_file)
    os.chdir(playlist_name)
    find_and_download_songs(reference_file)
    print("Operation complete.")
    return playlist_name

if __name__ == "__main__":
    main()

