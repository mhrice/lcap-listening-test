from flask import Flask, render_template, request, redirect, url_for
import os
import random
import glob
import datetime
import json
import getpass
from flask import Response

app = Flask(__name__)
# Define the upload folder
AUDIO_DIR = "static/audio"
app.config["Audio_DIR"] = AUDIO_DIR

file_a = ""
file_b = ""
file_x = ""
should_autoplay = False


@app.route("/")
def index():
    global file_a, file_b, file_x
    audio_files = []

    # Get all audio files
    for ext in ["**/*.flac", "**/*.mp3", "**/*.wav", "**/*.ogg", "**/*.aiff"]:
        audio_files.extend(
            glob.glob(os.path.join(app.config["Audio_DIR"], ext), recursive=True)
        )

    file_a, file_b, file_x = random.sample(audio_files, 3)
    print(file_a, file_b, file_x)
    return render_template(
        "index.html",
        file_a=file_a,
        file_b=file_b,
        file_x=file_x,
        should_autoplay=should_autoplay,
    )


@app.route("/submit", methods=["POST"])
def submit():
    global file_a, file_b, file_x
    if request.method == "POST":
        print(request.form)
        # Get button name
        button_text = request.form["data"]
        if button_text == "A is closer":
            print("A selected")
            answer = file_a
        elif button_text == "B is closer":
            print("B selected")
            answer = file_b
        output = {
            "A": file_a,
            "B": file_b,
            "X": file_x,
            "selected": answer,
            "user": getpass.getuser(),
        }
        fname = os.path.join(
            "submissions",
            datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S-%f") + ".json",
        )
        with open(fname, "w") as f:
            json.dump(output, f, indent=4)

    return redirect(url_for("index"))


@app.route("/play", methods=["POST"])
def play():
    global should_autoplay
    should_autoplay = True
    return Response(status=204)


@app.route("/pause", methods=["POST"])
def pause():
    global should_autoplay
    should_autoplay = False
    return Response(status=204)
