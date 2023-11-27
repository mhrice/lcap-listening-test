from flask import Flask, render_template, request, redirect, url_for
import os
import random
import glob
import datetime
import json
import getpass

app = Flask(__name__)
# Define the upload folder
AUDIO_DIR = "static/audio"
app.config["Audio_DIR"] = AUDIO_DIR

file_a = ""
file_b = ""
file_x = ""


@app.route("/")
def index():
    global file_a, file_b, file_x
    audio_files = glob.glob(
        os.path.join(app.config["Audio_DIR"], "**/*.wav"), recursive=True
    )
    file_a, file_b, file_x = random.sample(audio_files, 3)
    print(file_a, file_b, file_x)
    return render_template("index.html", file_a=file_a, file_b=file_b, file_x=file_x)


@app.route("/submit", methods=["POST"])
def submit():
    global file_a, file_b, file_x
    if request.method == "POST":
        print(request.form)
        # Get button name
        button_text = request.form["data"]
        if button_text == "X is A":
            print("A selected")
            answer = file_a
        elif button_text == "X is B":
            print("B selected")
            answer = file_b
        output = {"A": file_a, "B": file_b, "X": file_x, "selected": answer, "user": getpass.getuser()}
        fname = os.path.join("submissions", datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S-%f") + ".json")
        with open(fname, "w") as f:
            json.dump(output, f, indent=4)


    return redirect(url_for("index"))