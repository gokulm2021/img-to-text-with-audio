# AI-Based Image Classification and OCR System

## Overview

This project implements a web application that combines Optical Character Recognition (OCR) and Image Classification using Artificial Intelligence (AI). The system processes uploaded images to:
- **Extract text** using Tesseract OCR if present.
- **Classify objects** using a pre-trained MobileNetV2 model if no text is found.
- **Generate an audio description** of the image's content for improved accessibility, particularly for visually impaired users.

## Features

- **OCR (Optical Character Recognition)**: Detect and extract text from images using Tesseract.
- **Image Classification**: Classify objects in images with a pre-trained MobileNetV2 model.
- **Audio Output**: Generate audio responses for the detected text or classified object(s), using the `pyttsx3` library.
- **Web Interface**: Simple Flask web application for uploading images and receiving responses.

## Technologies Used

- **Flask**: Web framework to handle the backend and serve the application.
- **TensorFlow**: For loading the pre-trained MobileNetV2 model to classify images.
- **Tesseract OCR**: Open-source OCR engine for text extraction.
- **pyttsx3**: Python library for converting text to speech.
- **HTML/CSS/JavaScript**: For creating the frontend user interface.

## Installation

### Prerequisites

To run this project locally, ensure you have the following installed:

- **Python 3.x**
- **pip** (Python package manager)

### Step-by-step Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/AI-Image-Classification-OCR.git
    cd AI-Image-Classification-OCR
    ```

2. **Create a virtual environment (optional but recommended)**:
    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```
    - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

5. **Install Tesseract OCR**:
   - Download and install Tesseract from [here](https://github.com/tesseract-ocr/tesseract).
   - After installation, make sure to add Tesseract to your system’s PATH, or set the `pytesseract.pytesseract.tesseract_cmd` path in the code to the installation directory (as shown in the code).

6. **Run the Flask application**:
    ```bash
    python app.py
    ```

   The application will be accessible at `http://127.0.0.1:5000/` in your web browser.

## How to Use

1. Go to the web interface at `http://127.0.0.1:5000/`.
2. Upload an image using the **Upload Image** button.
3. The system will automatically:
   - Attempt to extract text from the image using OCR.
   - If no text is found, it will classify the image using the MobileNetV2 model.
4. The system will return a **text description** of the image content along with an **audio file** for listening to the description.

## File Structure

```plaintext
AI-Image-Classification-OCR/
│
├── app.py                    # Main Flask application
├── requirements.txt          # List of Python dependencies
├── static/                   
│   ├── uploads/              # Folder for storing uploaded images
│   └── output/               # Folder for storing generated audio files
├── templates/
│   └── index.html            # Frontend HTML file for the web interface
└── README.md                 # This readme file
