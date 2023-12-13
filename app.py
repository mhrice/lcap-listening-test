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
AUDIO_DIR = "static/audio/guitarset-pedalboard/inter-effect"
app.config["Audio_DIR"] = AUDIO_DIR

file_a = ""
file_b = ""
file_c = ""
file_x = ""
should_autoplay = False
random.seed(123)

# assume directory structure is:
# root_dir
#   inter-effect
#     effect1
#       file_a
#       file_b
#       file_c
#       file_x

#     effect2
#     ...
#   intra-effect
#     effect1
#     effect2
#     ...


# test case directories
test_dirs = glob.glob(os.path.join(AUDIO_DIR, "*"))
test_dirs = [d for d in test_dirs if os.path.isdir(d)]

# find example directories in each test_dir
dirs = []
for d in test_dirs:
    example_dirs = glob.glob(os.path.join(d, "*"))
    example_dirs = [d for d in example_dirs if os.path.isdir(d)]
    dirs.extend(example_dirs)

random.shuffle(dirs)  # shuffle the directory order
dir_index = 0  # keep track of which directory we're on


@app.route("/")
def root():
    return redirect(url_for("index", idx=dir_index))


@app.route("/<int:idx>")
def index(idx):
    global file_a, file_b, file_c, file_x, dirs, dir_index
    if idx >= len(dirs):
        return "Done!"
    dir_index = idx
    print(dir_index)
    d = dirs[dir_index]

    audio_files = []
    for ext in ["**/*.flac", "**/*.mp3", "**/*.wav", "**/*.ogg", "**/*.aiff"]:
        audio_files.extend(glob.glob(os.path.join(d, ext), recursive=True))

    file_a, file_b, file_c, file_x = sorted(audio_files[:4])
    print(file_a, file_b, file_c, file_x)

    # swap around the a, b, c files randomly
    files = [file_a, file_b, file_c]
    random.shuffle(files)
    file_a, file_b, file_c = files

    return render_template(
        "index.html",
        file_a=file_a,
        file_b=file_b,
        file_c=file_c,
        file_x=file_x,
        should_autoplay=should_autoplay,
        dir_index=dir_index,
        total_dirs=len(dirs),
    )


@app.route("/submit", methods=["POST"])
def submit():
    global file_a, file_b, file_c, file_x, dir_index
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
        elif button_text == "C is closer":
            print("C selected")
            answer = file_c
        output = {
            "A": file_a,
            "B": file_b,
            "C": file_c,
            "X": file_x,
            "selected": answer,
            "user": getpass.getuser(),
        }
        fname = os.path.join(
            "submissions",
            f"{dir_index}_{getpass.getuser()}.json",
        )
        with open(fname, "w") as f:
            json.dump(output, f, indent=4)
    if dir_index < len(dirs):
        dir_index += 1
    return redirect(url_for("index", idx=dir_index))


@app.route("/skip", methods=["POST"])
def skip():
    global file_a, file_b, file_c, file_x, dir_index
    output = {
        "A": file_a,
        "B": file_b,
        "C": file_c,
        "X": file_x,
        "selected": "DK",
        "user": getpass.getuser(),
    }
    fname = os.path.join(
        "submissions",
        f"{dir_index}_{getpass.getuser()}.json",
    )
    with open(fname, "w") as f:
        json.dump(output, f, indent=4)
    if dir_index < len(dirs):
        dir_index += 1
    return redirect(url_for("index", idx=dir_index))


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
