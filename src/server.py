
from flask import Flask, render_template, Response
from Camera import Camera

app = Flask(__name__)

cam = Camera(0)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/video_feed")
def video_feed():
    return Response(cam.stream(scale=0.25), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
