from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import os
import pyttsx3
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

# Configuration for file upload and output directories
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.config['OUTPUT_FOLDER'] = './static/output'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Set the path for Tesseract (make sure it's correct)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load pre-trained MobileNetV2 model for image classification
model = tf.keras.applications.MobileNetV2(weights='imagenet')

# Ensure necessary directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')  # Main upload page

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')  # Assuming you have a features.html page

@app.route('/contact')
def contact():
    return render_template('contact.html')  # Assuming you have a contact.html page

@app.route('/deaf')
def deaf():
    return render_template('deaf.html')  # Assuming you have a deaf.html page

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check if the file has an allowed extension
    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed. Please upload an image."}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    try:
        # Try to extract text from the image
        text = extract_text(filepath)
        if text.strip():  # If text is detected in the image
            audio_path = generate_audio(f"Text detected: {text}")
            return render_template('index.html', description=text, audio_path=audio_path, image_url=f'/static/uploads/{filename}')
        else:  # If no text is detected, classify the image
            description, detailed_info = classify_image(filepath)
            audio_path = generate_audio(f"The image is of a {description}.")
            return render_template('index.html', description=description, audio_path=audio_path, detailed_info=detailed_info, image_url=f'/static/uploads/{filename}')
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Function to extract text from an image using pytesseract
def extract_text(image_path):
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        print(f"Extracted text: {text}")  # Debugging: Check what text is extracted
        return text
    except Exception as e:
        raise Exception(f"Error in extracting text: {str(e)}")

# Function to classify the image using MobileNetV2
# Function to classify the image using MobileNetV2
def classify_image(image_path):
    try:
        # Open the image and convert to RGB if not already in RGB format
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Resize the image to 224x224 as required by MobileNetV2
        image = image.resize((224, 224))  
        
        # Convert the image to a numpy array and normalize pixel values to [0, 1]
        image_array = np.array(image) / 255.0
        
        # Expand dimensions to make it a batch of 1 image
        image_array = np.expand_dims(image_array, axis=0)

        # Predict the image class using the MobileNetV2 model
        predictions = model.predict(image_array)

        # Decode the predictions to get the class names and probabilities
        decoded_predictions = tf.keras.applications.mobilenet_v2.decode_predictions(predictions, top=5)[0]

        description = f"This is a {decoded_predictions[0][1]}."
        detailed_info = []

        # Collect detailed prediction information (class names and confidence scores)
        for pred in decoded_predictions:
            detailed_info.append({
                'class': pred[1],
                'confidence': pred[2]
            })

        print(f"Predicted description: {description}")  # Debugging: Check predicted description
        return description, detailed_info

    except Exception as e:
        raise Exception(f"Error in classifying image: {str(e)}")


# Function to generate audio from text using pyttsx3
def generate_audio(text):
    try:
        audio_filename = f'output_{np.random.randint(1, 100000)}.mp3'  # Unique filename
        audio_path = os.path.join(app.config['OUTPUT_FOLDER'], audio_filename)
        engine = pyttsx3.init()
        engine.save_to_file(text, audio_path)
        engine.runAndWait()
        print(f"Audio file generated: {audio_path}")  # Debugging: Check if audio is generated
        return f'/static/output/{audio_filename}'
    except Exception as e:
        raise Exception(f"Error in generating audio: {str(e)}")
    
@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Validate form data
        if not name or not email or not message:
            return render_template('index.html', error="All fields are required!")

        # Email credentials
        sender_email = "gokulapriyan1979@gmail.com"
        app_password = "syjj mzyk mlmv sypw"  # Use your generated app password here
        receiver_email = "gokulapriyan1979@gmail.com"  # Replace with your desired recipient email

        # Create the email content
        subject = "New Contact Form Submission"
        body = f"Name: {name}\nEmail: {email}\nMessage:\n{message}"

        # Create MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Replace with your email provider's SMTP server and port
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        # Return success with message for popup
        return render_template('contact.html', success="Message sent successfully!")

    except Exception as e:
        # Return error message for popup
        return render_template('contact.html', error=f"Failed to send message: {str(e)}")

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)
