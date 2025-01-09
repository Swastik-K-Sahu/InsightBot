import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from query import chatbot_response
from vectordb_loader import vectordb_loading

UPLOAD_FOLDER = 'data'
CHROMA_PATH = "chroma"
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['CHROMA_PATH'] = CHROMA_PATH
CORS(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload_file', methods=['POST'])
def set_dataset_file():
    
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        print("File uploaded")
        message = vectordb_loading()
        return jsonify({"message": message})
    else:
        return jsonify({"message": "Invalid file format. Only PDF files are allowed."}), 400

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    if user_input:
        bot_response = chatbot_response(user_input)
        return jsonify({"response": bot_response}), 200
    else:
        return jsonify({"response": "Please provide a valid input."}), 400
    
    
if __name__ == '__main__':
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['CHROMA_PATH']):
        os.makedirs(app.config['CHROMA_PATH'])
    app.run(debug=True, host='0.0.0.0', port=5000)
