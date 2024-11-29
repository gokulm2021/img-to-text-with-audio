from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import os
import pyttsx3
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['OUTPUT_FOLDER'] = './static/output'

# Path to Tesseract executable (update if Tesseract is installed elsewhere)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load pre-trained image classification model (e.g., MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights='imagenet')

@app.route('/')
def index():
    return render_template('index.html')

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

    # Perform OCR to extract text if any
    text = extract_text(filepath)

    if text.strip():
        # If text is detected, return the text
        audio_path = generate_audio(f"Text detected: {text}")
        return jsonify({"text": text, "audio_path": audio_path}), 200
    else:
        # If no text is detected, classify the image and provide more detailed info
        description, detailed_info = classify_image(filepath)
        audio_path = generate_audio(description)
        return jsonify({"description": description, "detailed_info": detailed_info, "audio_path": audio_path}), 200

def extract_text(image_path):
    """Extract text from an image using Tesseract OCR."""
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        return str(e)

def classify_image(image_path):
    """Classify the image using a pre-trained model (MobileNetV2) and return detailed classification info."""
    try:
        image = Image.open(image_path)
        image = image.resize((224, 224))  # Resize the image to fit model input size
        image = np.array(image) / 255.0  # Normalize the image
        image = np.expand_dims(image, axis=0)  # Add batch dimension

        # Predict the image using the MobileNetV2 model
        predictions = model.predict(image)

        # Decode the predictions to human-readable class labels
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]  # Top 5 predictions

        # Prepare the description based on the highest confidence
        description = f"This is a {decoded_predictions[0][1]} with a {decoded_predictions[0][2]*100:.2f}% probability."
        detailed_info = []

        # Add the detailed information for top predictions
        for pred in decoded_predictions:
            detailed_info.append({
                'class': pred[1],  # Object class label
                'probability': f"{pred[2]*100:.2f}%"  # Probability score
            })

        return description, detailed_info
    except Exception as e:
        return "Error in image classification.", []

def generate_audio(text):
    """Generate audio file from text using pyttsx3."""
    audio_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.mp3')
    engine = pyttsx3.init()
    engine.save_to_file(text, audio_path)
    engine.runAndWait()
    return f'/static/output/output.mp3'

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
    app.run(debug=True)
