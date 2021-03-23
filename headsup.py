# Created by Patrick Kao
# inst = spotipy.Spotify()
# playlist = inst.search(q="playlist:Tween White Girl Jams", type="playlist")
# print(playlist)
import datetime
import random

import spotipy

# web console https://developer.spotify.com/console/get-current-user-playlists/

user_id = "mutleythebookworm"
playlist_name = "TBT"

auth_manager = spotipy.SpotifyClientCredentials(client_id="7c8c15002eed4cb79b8b36b527427842",
                                                client_secret="7e9ee0ea788341dda371d4e53c1b648d")
sp = spotipy.Spotify(auth_manager=auth_manager)

playlists = sp.user_playlists(user=user_id, limit=50)

play_id = None

for item in playlists["items"]:
    if item["name"] == playlist_name:
        play_id = item["id"]
        break


def get_playlist_tracks(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


songs = get_playlist_tracks(user_id, play_id)
names = []
for song in songs:
    names.append(song["track"]["name"])

random.shuffle(names)

cur_pos = 0

score = 0
time_limit = datetime.timedelta(0, 120)
start_time = datetime.datetime.now() - time_limit * 2
while True:
    remaining_time = time_limit - (datetime.datetime.now() - start_time)
    print(f"Time left: {remaining_time}")
    if datetime.datetime.now() - start_time > time_limit:
        # new game
        print(f"Game over! Score was: {score}")
        score = 0
        input("Enter any text to continue")
        start_time = datetime.datetime.now()

    cur_pos += 1
    print(f"Current song: {names[cur_pos]}")
    result = input()
    if "d" in result:
        score += 1

    if "w" in result:
        score += 1
        continue

    if "s" in result:
        continue
