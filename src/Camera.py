from imutils import paths
import cv2
from statistics import mean
import numpy as np

from Face import Face


class Camera:
    """
    Class to handle camera and frame actions

    Args:
    cam_id: Id of the used camera. 
        To find out the camera id run 'ls -ltrh /dev/video*' command. 
        If you use the docker image you have to pass it: 'dev/videoX:/dev/video0'
    faces: Face object to handle encodings and face search

    """

    def __init__(self, cam_id:int, faces:Face):
        self.camera = cv2.VideoCapture(cam_id)
        self.__ramp_up()
        self.faces = faces

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


    def _draw_circle(self, image:np.ndarray, coords:tuple, scale:float,
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

    def _add_name(self, image:np.ndarray, name:str, coords:tuple, 
                  scale:float, color:tuple):
        """
        Write the given name to the picture

        Args:
        image: Image from the webcam
        name: name to 
        coords: Location of faces on the image
        scale: Scaling of the imput image before forvarded to be encoded
        color: Color of the drawn circle in (B, G, R) formatted tuple

        """

        # Calulate the scale multiplier
        scale_multiplyer = 1 / scale

        # Get upscaled coordinates
        top, left, bot, right = [coord * scale_multiplyer for coord in coords]

        # Calulate the target coords
        position = (int(left) - 10, int(bot))

        # Write text to the image
        cv2.putText(image, name, position, cv2.FONT_HERSHEY_DUPLEX, 1, color, 3)




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
        locations, face_encodings = self.faces.encode_image(small_image)

        # Draw circles on the full frame
        for enc, loc in zip(face_encodings, locations):
            full_image = self._draw_circle(
                    full_image, loc, scale, color, thickness
                )
            name = self.faces.get_matching_face(enc)

            self._add_name(full_image, name, loc, scale, color)

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
