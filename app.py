from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import os
import pyttsx3
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['OUTPUT_FOLDER'] = './static/output'

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
model = tf.keras.applications.MobileNetV2(weights='imagenet')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    text = extract_text(filepath)

    if text.strip():
        audio_path = generate_audio(f"Text detected: {text}")
        return jsonify({"text": text, "audio_path": audio_path}), 200
    else:
        description, detailed_info = classify_image(filepath)
        audio_path = generate_audio(description)
        return jsonify({"description": description, "detailed_info": detailed_info, "audio_path": audio_path}), 200

def extract_text(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)

def classify_image(image_path):
    try:
        image = Image.open(image_path)
        image = image.resize((224, 224))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0)

        predictions = model.predict(image)
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]

        description = f"This is a {decoded_predictions[0][1]}."
        detailed_info = []

        for pred in decoded_predictions:
            detailed_info.append({
                'class': pred[1]
            })

        return description, detailed_info
    except Exception as e:
        return "Error in image classification.", []

def generate_audio(text):
    audio_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.mp3')
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    return f'/static/output/output.mp3'

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True)
