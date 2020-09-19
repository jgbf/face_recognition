from imutils import paths
import face_recognition as frec
import cv2
from statistics import mean
import numpy


class Camera:

    def __init__(self, cam_id):
        self.camera = cv2.VideoCapture(cam_id)
        self.__ramp_up()

    def __del__(self):
        self.camera.release()

    def _read_image(self, scale:float):
        """
        Read one image from the camera and resize it and convert it to an RGB 
        image from the default BGR waht open cv uses.

        Args:
        scale: Scaling of the imput image before forvarded to be encoded

        Returns with a downscaled image for encoding and the raw image to be 
        processed later.

        """

        # Read one frame from the camera
        ret, frame = self.camera.read()

        # Scale down the image
        small_frame = cv2.resize(frame, (0, 0), fx=scale, fy=scale)

        # Convert scaled image to rgb 
        rgb_frame = small_frame[:, :, ::-1]

        return rgb_frame, frame

    def __ramp_up(self, ramp:int=3):
        """
        When you initialize a camera with open cv the first pictures are really 
        dark so you need to ramp it up to see something on the picture.
        
        Args:
        ramp: number of ramping images on camera init
        
        """

        for i in range(ramp):
            self.camera.read()


    def _encode_image(self, image:numpy.ndarray):
        """
        Find faces on the image and calculate the encodings of the find images
        
        Args:
        image: Downscaled image from the camera

        """

        # Get face locations on the given image
        locations = frec.face_locations(image)

        # Encode images on the given locations
        encodings = frec.face_encodings(image, locations)

        return locations, encodings


    def _draw_circle(self, image:numpy.ndarray, coords:tuple, scale:float,
                    color:tuple=(205, 205, 205), thickness:int=2):
        """
        Draw a circle to the full frame image based on the found face on the 
        downscaled image.

        Args:
        image: Image from the webcam
        coords: Location of faces on the image
        scale: Scaling of the imput image before forvarded to be encoded
        color: Color of the drawn circle in (B, G, R) formatted tuple
        thickness: Thickness of the drawn circle

        """

        # Get the scale multiplyer from down scaling 
        scale_multiplyer = 1 / scale

        # Get upscaled coords
        top, left, bot, right = [coord * scale_multiplyer for coord in coords]

        # Calulate the center of the face circle
        center = (int(mean([left, right])), int(mean([top, bot])))

        # Calulate the radius of the face circle
        radius = max(center[0] - right, bot - center[1])
        # Make the radius a little bigget to prevent face covering
        radius = int(radius * 1.1)

        # Draw the circle on the image
        drawn_image = cv2.circle(image, center, radius, color, thickness)
        
        return drawn_image

    def get_marked_image(self, scale:float=0.5, color:tuple=(205, 205, 205), 
                         thickness:int=2):
        """
        Read an image identify faces and draw a circle around them.

        Args:
        scale: Scaling of the imput image before forvarded to be encoded
        color: Color of the drawn circle in (B, G, R) formatted tuple
        thickness: Thickness of the drawn circle

        """

        # Get frames from camera
        small_image, full_image = self._read_image(scale)

        # Find and encode faces
        locations, face_encodings = self._encode_image(small_image)

        # Draw circles on the full frame
        for loc in locations:
            full_image = self._draw_circle(
                    full_image, loc, scale, color, thickness
                )

        return full_image

    def stream(self, scale:float=0.5, color:tuple=(205, 205, 205), 
               thickness:int=2):

        """
        Stream marked images in the right jpeg byte format

        Args:
        scale: Scaling of the imput image before forvarded to be encoded
        color: Color of the drawn circle in (B, G, R) formatted tuple
        thickness: Thickness of the drawn circle

        """

        while True:
            frame = self.get_marked_image(scale, color, thickness)
            ret, jpeg = cv2.imencode(".jpg", frame)

            byte_coded = jpeg.tobytes()

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n\r\n" + byte_coded + b"\r\n\r\n"
                )
