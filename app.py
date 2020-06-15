# Local modules
from modules.PIL_handler import *

# Vanilla modules
import os

# Installed modules
from flask import Flask, render_template, redirect, url_for, request, send_file
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__)

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']
UPLOAD_FOLDER = os.path.join(os.getcwd() + "/static/uploads/")

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def main():
    filelist = [f for f in os.listdir(UPLOAD_FOLDER) if not f.endswith(".keep")]
    for f in filelist:
        os.remove(os.path.join(UPLOAD_FOLDER, f))

    return render_template("index.html")

@app.route("/verificate", methods=["GET", "POST"])
def verification():
    if request.method == "POST":
        image = request.files["file"]
        if "Resize" in request.form and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for("resize", image=filename))
        elif "Convert" in request.form and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for("convert", image=filename))
        else:
            return render_template("error.html", error="The file uploaded is not an allowed extension.")
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
    app.run(debug=True)
