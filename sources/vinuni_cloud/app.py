from flask import Flask
from flask import render_template, request, jsonify, send_file
from werkzeug.debug import DebuggedApplication

import os
import logging

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 # Max image size: 2MB
app.config['UPLOAD_FOLDER'] =  os.path.join(os.getcwd(), 'uploads') # Save images to the 'uploads' folder
ALLOW_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOW_EXTENSIONS

def format_size(size):
    if size < 1024:
        return f"{size} bytes"
    elif size < 1024 * 1024:
        return f"{round(size / 1024, 2)} KB"
    else:
        return f"{round(size / (1024 * 1024), 2)} MB"

@app.route('/')
def home():
    if request.args.get('file'):
        try:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], request.args.get('file'))
            if os.path.exists(filename):
                if os.access(filename, os.R_OK):
                    # if the file is not image, error with the content of the file
                    if not allowed_file(filename):
                        content = open(filename, 'rb').read()
                        return jsonify({"error": "not image", "file_name": filename, "file": content.decode('utf-8')}), 200
                    return send_file(filename, as_attachment=True)
                    
                return jsonify({"message": "File cannot read"}), 500
            return jsonify({"message": "File not found"}), 404
        except:
            pass
    return render_template("index.html") 


@app.route("/files", methods=["GET"])
def get_all_files():
    data = []
    try:
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                file_size = format_size(file_size)
                splitted = file.split(".")
                file_name = splitted[0:len(splitted) - 1]
                file_type = splitted[-1]
                data.append({
                    "file_name": file_name,
                    "file_type": file_type,
                    "file_size": file_size
                })
    except:
        pass
    return jsonify({"data": data}), 200


@app.route('/upload', methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    filename = file.filename
    size = file.content_length
    if size > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({'message': 'Your file upload is over 2MB'}), 400
    if file and allowed_file(filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200

# @app.route("/console", methods=["GET"])

if __name__ == '__main__':
    app.debug = True
    app.wsgi_app = DebuggedApplication(app, evalex=True)
    app.run(port=5000, host="0.0.0.0")