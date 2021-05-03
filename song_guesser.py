# Created by Patrick Kao
# inst = spotipy.Spotify()
# playlist = inst.search(q="playlist:Tween White Girl Jams", type="playlist")
# print(playlist)
import datetime
import random

import spotipy


# web console https://developer.spotify.com/console/get-current-user-playlists/

def _get_playlist_tracks(sp, user_id, playlist_id):
    results = sp.user_playlist_tracks(user_id, playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks


def _get_playlist_id(sp, user_id, playlist_name):
    results = sp.user_playlists(user=user_id, limit=50)
    while True:
        for item in results["items"]:
            if item["name"] == playlist_name:
                return item["id"]
        if results["next"]:
            results = sp.next(results)
        else:
            raise ValueError(f"Couldn't find playlist {playlist_name}")


def get_tracks(user_id, playlist_name, use_suggestions=False):
    auth_manager = spotipy.SpotifyClientCredentials(client_id="7c8c15002eed4cb79b8b36b527427842",
                                                    client_secret="7e9ee0ea788341dda371d4e53c1b648d")
    sp = spotipy.Spotify(auth_manager=auth_manager)
    playlist_id = _get_playlist_id(sp, user_id, playlist_name)
    songs = _get_playlist_tracks(sp, user_id, playlist_id)
    tracks = []
    for song in songs:
        artist = song["track"]["artists"][0]["name"]
        artist_id = song["track"]["artists"][0]["id"]
        track_id = song["track"]["id"]
        if not use_suggestions:
            tracks.append((song["track"]["name"], artist))
        else:
            tracks.append(track_id)

    if use_suggestions:
        random.shuffle(tracks)
        recommendations = sp.recommendations(seed_tracks=tracks[:5], limit=99)
        return [(rec["name"], rec["artists"][0]["name"]) for rec in recommendations["tracks"]]

    random.shuffle(tracks)
    return tracks


def play_game(tracks):
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
        print(f"Current song: {tracks[cur_pos][0]}")
        print(f"Artist: {tracks[cur_pos][1]}")
        result = input()
        if "d" in result:
            score += 1

        if "w" in result:
            score += 1
            continue

        if "s" in result:
            continue


if __name__ == "__main__":
    USER_ID = "dolphonie"
    PLAYLIST_NAME = "New Playlist"
    USE_SUGGESTIONS = True

    tracks = get_tracks(USER_ID, PLAYLIST_NAME, USE_SUGGESTIONS)
    play_game(tracks)
