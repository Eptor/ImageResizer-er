# Local modules
from modules.PIL_handler import *

# Vanilla modules
import os

# Installed modules
from flask import Flask, render_template, redirect, url_for, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(os.getcwd() + "/static/uploads/")

@app.route("/")
def main():
    filelist = [f for f in os.listdir(UPLOAD_FOLDER) if not f.endswith(".keep")]
    for f in filelist:
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    return render_template("index.html")

@app.route("/verificate", methods=["GET", "POST"])
def verification():
    if request.method == "POST":
        if "Resize" in request.form:
            image = request.files["file"]
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for("resize", image=filename))
        elif "Convert" in request.form:
            image = request.files["file"]
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for("convert", image=filename))
    else:
        return redirect("main")

@app.route("/resize/<image>")
def resize(image):
    img = Image.open(os.path.join(UPLOAD_FOLDER,image))
    width, height = img.size
    img = img.resize((width // 2, height // 2), Image.LANCZOS)
    img.save(os.path.join(UPLOAD_FOLDER,image))
    return send_file(os.path.join(os.path.join(UPLOAD_FOLDER,image)), as_attachment=True)

@app.route('/convert/<image>')
def convert(image):
    img = Image.open(os.path.join(UPLOAD_FOLDER,image))
    width, height = img.size
    img = img.resize((width // 2, height // 2), Image.LANCZOS)
    name = f"{os.path.splitext(image)[0]}.png"
    img.save(os.path.join(UPLOAD_FOLDER,name))
    return send_file(os.path.join(os.path.join(UPLOAD_FOLDER,name)), as_attachment=True)


if __name__ == '__main__':
    app.run()
