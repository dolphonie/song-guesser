import datetime

from flask import Flask, render_template, request, session
from flask_session import Session

from song_guesser import get_tracks

app = Flask(__name__)
app.secret_key = "8DSF0987uQ@#$VFZ3d"
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_THRESHOLD'] = 1e5
Session(app)

def get_time():
    time_limit = datetime.timedelta(0, 120)
    remaining_time = time_limit - (datetime.datetime.now() - session["start_time"])
    return remaining_time, datetime.datetime.now() - session["start_time"] > time_limit

def render(time_left, out):
    if not out:
        cur_song = session["tracks"][session["cur_pos"]]
        return render_template("lobby.html",
                               song=cur_song[0],
                               artist=cur_song[1],
                               score=session["score"],
                               time_left=time_left)
    else:
        return render_template("game_over.html", score=session["score"])


def reset_session():
    session["score"] = 0
    session["start_time"] = datetime.datetime.now()


@app.route("/", methods=["POST", "GET"])
def main():
    if "songs" not in session:
        USER_ID = "dolphonie"
        PLAYLIST_NAME = "guesser subset"
        USE_SUGGESTIONS = False
        SUGGESTION_COUNT = 500
        tracks = get_tracks(USER_ID, PLAYLIST_NAME, USE_SUGGESTIONS, SUGGESTION_COUNT)
        session["tracks"] = tracks
        session["cur_pos"] = 0
        reset_session()

    time_left, out = get_time()
    return render(time_left, out)


@app.route("/success", methods=["POST", "GET"])
def success():
    session["cur_pos"] += 1
    session["score"] += 1
    time_left, out = get_time()
    return render(time_left, out)


@app.route("/skip", methods=["POST", "GET"])
def skip():
    session["cur_pos"] += 1
    time_left, out = get_time()
    return render(time_left, out)


@app.route("/increment", methods=["POST", "GET"])
def increment():
    session["score"] += 1
    time_left, out = get_time()
    return render(time_left, out)

@app.route("/restart", methods=["POST", "GET"])
def restart():
    reset_session()
    time_left, out = get_time()
    return render(time_left, out)

app.run(host='localhost', port=5000)
