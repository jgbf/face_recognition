import face_recognition as fr
import Database
import cv2
import numpy as np
import os


class Face:
    """
    Class to store known faces and handle face encodings and

    Args: 
    db: Database object to connect to the face database
    strictness: Strictness of the face comparison

    """

    def __init__(self, db:Database, strictness:float=0.5):
        self.db = db
        self.known_faces = self.db.load_faces()
        self.strictness = strictness

    def encode_image(self, image:np.ndarray):
        """
        Find faces on the image and calculate the encodings of the find images
        
        Args:
        image: Downscaled image from the camera

        """

        # Get face locations on the given image
        locations = fr.face_locations(image)

        # Encode images on the given locations
        encodings = fr.face_encodings(image, locations)

        return locations, encodings

    def save_face(self, name:str, encoding:np.ndarray):
        """
        Save new face to the database and in the memory too.

        Args:
        name: Name of the new face
        encoding: Encoding for the new face

        """

        # Save face to memory
        self.known_faces["encodings"].append(encoding)
        self.known_faces["names"].append(name)

        # Save face data to database
        self.db.store_face(name, encoding)

    def get_matching_face(self, encoding:np.ndarray):
        """
        Get the name of the closest face in the database

        Args:
        encoding: encoding of a face 
        
        """

        # Calculate similatrity level for all stored faces 
        distances = fr.face_distance(self.known_faces["encodings"], encoding)
        # Get the index of the best matching face
        best_match_index = np.argmin(distances)
        # Set default name
        name = "Unknown"

        # Select the best matching face from known faces
        if distances[best_match_index] < self.strictness:
            name = self.known_faces["names"][best_match_index]

        return name

    def read_image(self, path):
        """
        Read image from a given path with OpenCV

        Args:
        path: Path to image

        """
        return cv2.imread(path, 1)

    def learn_face(self, path, name):
        """
        Save face from an image to the database

        Args:
        path: Path to source file
        name: Name associated with the savable face

        """
        
        # Read image from drive
        image = self.read_image(path)
        # Remove image from disk
        os.remove(path)
        # Get face locations and encodings from image
        coords, encodings = self.encode_image(image)
        
        # Set default index
        selected_index = 0

        # Get the biggest face on image
        if len(encodings) > 1:
            max_size = 0

            for idx, coord in enumerate(coords):
                # The biggest face is the one whit hte biggest area
                size = (coord[2] - coord[0]) * (coord[1] - coord[3])
                
                if size > max_size:
                    max_size = size
                    selected_index = idx

        self.save_face(name, encodings[selected_index])
