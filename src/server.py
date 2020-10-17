
from flask import Flask, render_template, Response, request, flash

from Camera import Camera
from Database import Database
from Face import Face
from Uploader import Uploader


app = Flask(__name__)
app.secret_key="aaaaaaa"
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
            success = face.learn_face(filename, name)
            print(success)
            if success:
                flash(f"New face saved to database: {name}", "success")
            else:
                flash(f"No detected face on image", "warning")

    return render_template("upload.html")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
