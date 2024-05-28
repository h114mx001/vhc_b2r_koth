from flask import Flask
from flask import render_template
import os 
app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html") 

@app.route('/upload', methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': f'File {filename} uploaded successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)