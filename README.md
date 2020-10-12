![versions](https://img.shields.io/pypi/pyversions/pybadges.svg)

# Face recognition demo
This project is based on python *face_recognition* package. You can run it in a docker container or directly with python. The code is tested on Pop!_OS. It should work on any Linux based operation system.
In the future I plan to test it on Windows and on WSL2.

## Install and run
 Open terminal and move to the cloned repository.
### Docker
 1. **Build image**
    ```bash
    docker build -t <image_name> .
    ```
 2. **Run image**
    ```bash
    docker run -p <your_port>:5000 --device /dev/video<camera_number>:/dev/video0
    ```

### Python
1. **Create a virtualenv**
    ```bash
    virtualenv <env_name> -p 3
    ```
    This command will create a new directory in the actual folder.
    
2. **Activate new venv**
    ```bash
    source <env_name>/bin/bash
    ```
    After this command you should see the name of the activated venv at the beginning of the terminal line.
3. **Install dependencies**
    ```bash
    python -m pip install -r requirements.txt
    ```
4. **Run server**
    ```bash
    python src/server.py
    ```
**Note:** 
- You can use any free port to run the server as your_port value.
- Default camera_number is 0 on your computer. To fin out camera device id-s run ```ls -ltrh /dev/video*```

## Usage:
If everything went well during the previous step you will be able to check the running application in your browser. Just open ```127.0.0.1:<your_port>``` address.

### There are 2 main routes:
- **index:** Here you can see the live video feed with the detected faces highlighted and the recognized faces marked with the stored name.
- **/register:** You can register new faces with a name by uploading an image of his/her face. If you upload a picture with more faces on it the face registration mechanism is selecting the face witch covers the biggest area on the image.

