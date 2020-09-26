import sqlite3
from datetime import datetime as dt
import json
import uuid


class Database():
    """
    Class to handle database connection 

    Args:
    db_file: path to the database file 

    """

    def __init__(self, db_file:str="face_database.db"):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Check if the face database existence
        self.cursor.execute(
            """
            SELECT count(name) 
            FROM sqlite_master 
            WHERE type='table' AND name='faces'
            """
        )

        if self.cursor.fetchone()[0] == 0:
            # Create the faces table 
            self.cursor.execute(
                "CREATE TABLE faces (id, created_at, name, encoding)"
            )

            # Commit changes
            self.conn.commit()

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def load_faces(self):
        """
        Load all faces and face encodings from database and returns with a 
        dictionary with a name and an ecoding list. 
        (It will be handy when you use face_distance method on encodings)

        """

        self.cursor.execute("SELECT * FROM faces")
        raw_data = self.cursor.fetchall()

        encodings = []
        names = []

        for row in raw_data:
            encodings.append(json.loads(row[3]))
            names.append(row[2])

        return {"names": names, "encodings": encodings}

    def store_face(self, name, encoding):
        """
        Save the given name and the connected encoding to the database

        Args:
        name: Name of the new face
        encoding: The encoding of the new face

        """

        # Generate random id for face
        fid = uuid.uuid1()
        # Get actual time to keep track of the face addition times
        time = str(dt.now())
        # json dump the face encodings
        enc_dump = json.dumps(list(encoding))
        # Insert face to the database
        self.cursor.execute(
            f"""INSERT INTO faces 
                VALUES ('{fid}','{time}', '{name}', '{enc_dump}')"""
        )
        # Commit changes to to the database
        self.conn.commit()
