from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from __init__ import removeBg
import uuid

app = Flask(__name__, static_folder='static')
CORS(app)

UPLOAD_FOLDER = 'static/inputs'
RESULTS_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/remove-background', methods=['POST'])
def remove_background():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        result = removeBg(filepath)
        if result == "---Success---":
            result_filename = filename.rsplit('.', 1)[0] + '.png'
            return jsonify({
                'success': True,
                'resultUrl': f'/static/results/{result_filename}'
            })
        
        return jsonify({'error': 'Processing failed'}), 500
        
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/images', methods=['GET'])
def get_images():
    results = []
    for filename in os.listdir(RESULTS_FOLDER):
        if filename.endswith('.png'):
            results.append({
                'id': filename.rsplit('.', 1)[0],
                'originalUrl': f'/static/inputs/{filename.rsplit(".", 1)[0]}.jpg',
                'resultUrl': f'/static/results/{filename}'
            })
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)