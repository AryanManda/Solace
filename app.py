from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import time
import requests
import google.generativeai as genai 

from image_classifier import classify_image

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = "KEY" 
genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel('gemini-1.5-pro')



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')

      
        response = model.generate_content(user_message)

     
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


@app.route('/classify-image', methods=['POST'])
def classify_image_route():
    print("[app.py] Entered classify_image_route") 

    if 'image' not in request.files:
        print("[app.py] No 'image' file part in request.")
        return jsonify({'error': 'No image file provided.'}), 400

    image = request.files['image']
    if image.filename == '':
        print("[app.py] No selected file.") 
        return jsonify({'error': 'No selected image file.'}), 400

    uploads_dir_relative = 'uploads'
    uploads_dir_absolute = os.path.join(os.getcwd(), uploads_dir_relative)

    if not os.path.exists(uploads_dir_absolute):
        try:
            os.makedirs(uploads_dir_absolute)
            print(f"[app.py] Created uploads directory: {uploads_dir_absolute}") 
        except OSError as e:
            print(f"[app.py] Error creating uploads directory {uploads_dir_absolute}: {e}")
            return jsonify({'error': f'Server error creating upload directory: {e}'}), 500

    
    image_filename = os.path.basename(image.filename)
    image_path_absolute = os.path.join(uploads_dir_absolute, image_filename)

    print(f"[app.py] Attempting to save file to absolute path: {image_path_absolute}")

    try:
        # Attempt to save the file
        image.save(image_path_absolute)
        print(f"[app.py] File saved successfully to {image_path_absolute}") # Debug print

        try:
            
            print(f"[app.py] Calling classify_image with path: {image_path_absolute}") 
            result = classify_image(image_path_absolute) 
            print(f"[app.py] classify_image returned: {result}") 

            return jsonify({'result': result}) 

        except Exception as e:
           
            print(f"[app.py] Error during image classification process (inside try block): {e}") 
            import traceback 
            traceback.print_exc() 
            return jsonify({'error': f'Error during image classification: {e}'}), 500

    except Exception as e: 
        print(f"[app.py] Error during file saving or initial processing in /classify-image route: {e}") # Debug print
        import traceback
        traceback.print_exc() 
        return jsonify({'error': f'Server error processing file: {e}'}), 500

    finally:
        if os.path.exists(image_path_absolute):
            try:
                os.remove(image_path_absolute)
                print(f"[app.py] Cleaned up temporary file: {image_path_absolute}") # Debug print
            except OSError as e:
                print(f"[app.py] Error cleaning up file {image_path_absolute}: {e}") # Debug print


if __name__ == '__main__':
    app.run(debug=True) 
