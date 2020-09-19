
from image_function import *
import cv2

from flask import Flask, make_response
server = Flask(__name__)

@server.route("/")
def main():
    cam = Camera(0)

    circled = cam.get_marked_image()

    # Encode Raw file
    ret, jpeg = cv2.imencode(".jpg", circled)
    response = make_response(jpeg.tobytes())
    response.headers['Content-Type'] = 'image/jpeg'

    return response

if __name__=="__main__":
    server.run(host='0.0.0.0', port=5000)
