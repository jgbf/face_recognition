import os
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename


class Uploader():
    """
    File uplad handler oblject

    Args:
    app: Falsk object of the main app
    folder_path: Path to the temporary upload folder

    """

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

    def __init__(self, app:Flask, folder_path:str="."):
        self.folder_path = folder_path
        self.app = app

    def allowed_file(self, filename):
        return '.' in filename and \
                filename.rsplit('.', 1)[1].lower() in Uploader.ALLOWED_EXTENSIONS

    def upload(self):
        if request.method == 'POST':
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(
                    os.path.join(
                        self.app.config['UPLOAD_FOLDER'], 
                        filename
                    )
                )

                return filename, request.form["name"]
