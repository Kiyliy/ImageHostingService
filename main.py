"""
一步一步来创建一个简单的图床应用使用Python和Flask
"""

from flask import Flask, request, send_from_directory, jsonify, abort
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({'error': '没有文件部分'}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': '没有选择文件'}), 400
    if file and allowed_file(file.filename):
        extension = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{uuid.uuid4()}.{extension}"
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'id': filename}), 200
    else:
        return jsonify({'error': '不允许的文件类型'}), 400

@app.route('/photo/<id>', methods=['GET'])
def get_photo(id):
    if os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], id)):
        return send_from_directory(app.config['UPLOAD_FOLDER'], id)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
