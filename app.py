from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import time
import requests
import google.generativeai as genai # Import the Gemini library

from image_classifier import classify_image

app = Flask(__name__)
CORS(app)

# Configure Google Gemini API
# Get your API key from https://makersuite.google.com/app/apikey
GEMINI_API_KEY = "AIzaSyDHQYWUhd0Fhk-t7VxB_EVMjT_oPN6IrOs" # <-- Replace with your Gemini API Key
genai.configure(api_key=GEMINI_API_KEY)

# Initialize the generative model
# You can choose a different model if needed, e.g., 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-1.5-pro')

# Hugging Face API configuration (keeping it commented out for now)
# API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
# headers = {"Authorization": "Bearer hf_xxx"}  # Replace with your Hugging Face API token

# def query_huggingface(payload):
#     response = requests.post(API_URL, headers=headers, json=payload)
#     return response.json()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

        # Generate response using Gemini API
        # Use a conversation history if you want the model to remember previous turns
        # For simplicity, this example treats each turn as independent
        response = model.generate_content(user_message)

        # Extract the response text
        # Gemini response structure might vary, adjust based on API output
        ai_response = response.text

        return jsonify({
            'response': ai_response,
            'status': 'success'
        })

    except Exception as e:
        print(f"Error in chat route: {e}")
        return jsonify({
            'error': str(e),
            'status': 'error'
        }), 500

# --- Image Classification Route (Uncommented and with improved error handling) ---
# Make sure 'classify_image' is imported if you keep this route active.
# from image_classifier import classify_image # This import is now at the top

@app.route('/classify-image', methods=['POST'])
def classify_image_route():
    print("[app.py] Entered classify_image_route") # Debug print

    # --- Input Validation ---
    if 'image' not in request.files:
        print("[app.py] No 'image' file part in request.") # Debug print
        return jsonify({'error': 'No image file provided.'}), 400

    image = request.files['image']
    if image.filename == '':
        print("[app.py] No selected file.") # Debug print
        return jsonify({'error': 'No selected image file.'}), 400

    # --- Directory Creation ---
    uploads_dir_relative = 'uploads'
    uploads_dir_absolute = os.path.join(os.getcwd(), uploads_dir_relative) # Get absolute path

    if not os.path.exists(uploads_dir_absolute):
        try:
            os.makedirs(uploads_dir_absolute)
            print(f"[app.py] Created uploads directory: {uploads_dir_absolute}") # Debug print
        except OSError as e:
            print(f"[app.py] Error creating uploads directory {uploads_dir_absolute}: {e}") # Debug print
            return jsonify({'error': f'Server error creating upload directory: {e}'}), 500

    # --- File Saving ---
    # Sanitize filename to prevent directory traversal issues (basic security)
    image_filename = os.path.basename(image.filename)
    image_path_absolute = os.path.join(uploads_dir_absolute, image_filename)

    print(f"[app.py] Attempting to save file to absolute path: {image_path_absolute}") # Debug print

    try:
        # Attempt to save the file
        image.save(image_path_absolute)
        print(f"[app.py] File saved successfully to {image_path_absolute}") # Debug print

        # --- Image Classification ---
        # Call the image classification function from image_classifier.py
        # Ensure classify_image is imported and the model is loaded within image_classifier.py
        try:
            # Add a small delay just before classification, if needed for file system sync
            # time.sleep(0.1) # Uncomment this if you still get file not found errors during classification
            print(f"[app.py] Calling classify_image with path: {image_path_absolute}") # Debug print
            result = classify_image(image_path_absolute) # Call the classification function
            print(f"[app.py] classify_image returned: {result}") # Debug print

            return jsonify({'result': result}) # Return classification result

        except Exception as e:
            # Catch errors specifically during the classification function call
            print(f"[app.py] Error during image classification process (inside try block): {e}") # Debug print
            import traceback # Import traceback for detailed error info
            traceback.print_exc() # Print the full traceback to the terminal
            return jsonify({'error': f'Error during image classification: {e}'}), 500

    except Exception as e: # Catch errors during file saving or other initial steps
        print(f"[app.py] Error during file saving or initial processing in /classify-image route: {e}") # Debug print
        import traceback
        traceback.print_exc() # Print the full traceback
        return jsonify({'error': f'Server error processing file: {e}'}), 500

    finally:
        # --- File Cleanup ---
        # Clean up the temporary file using absolute path
        if os.path.exists(image_path_absolute):
            try:
                os.remove(image_path_absolute)
                print(f"[app.py] Cleaned up temporary file: {image_path_absolute}") # Debug print
            except OSError as e:
                print(f"[app.py] Error cleaning up file {image_path_absolute}: {e}") # Debug print


if __name__ == '__main__':
    app.run(debug=True) 