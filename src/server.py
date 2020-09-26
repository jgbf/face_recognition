
from flask import Flask, render_template, Response, request

from Camera import Camera
from Database import Database
from Face import Face
from Uploader import Uploader


app = Flask(__name__)
UPLOAD_FOLDER = "."
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = Database()
face = Face(db)
cam = Camera(0, face)
uploader = Uploader(app, UPLOAD_FOLDER)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(
            cam.stream(scale=0.3), 
            mimetype="multipart/x-mixed-replace; boundary=frame"
        )

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        filename, name = uploader.upload()

        if filename:
            face.learn_face(filename, name)

    return render_template("upload.html")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
