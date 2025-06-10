import tensorflow as tf
import os
# import cv2 # Remove cv2 import
import numpy as np
import time
from PIL import Image # Import Pillow

# Load the trained model (assuming it's saved as 'imageclassificationapplication.h5' in a 'models' folder)
# Make sure the 'models' folder exists in your project directory
# If your model is saved elsewhere, update this path
model_path = os.path.join('models', 'imageclassificationapplication.h5')
# Check if the model file exists before loading
if not os.path.exists(model_path):
    print(f"Error: Model file not found at {model_path}")
    # You might want to raise an error or handle this more gracefully
    # For now, we'll assume the model is there

try:
    # Adding a small delay before loading model just in case
    # time.sleep(0.5) # Uncomment if model loading still has issues
    model = tf.keras.models.load_model(model_path)
    print("Image classification model loaded successfully.")
except Exception as e:
    print(f"Error loading image classification model: {e}")
    import traceback
    traceback.print_exc()
    model = None # Set model to None if loading fails

def classify_image(image_path):
    print(f"[classify_image] Function called with path: {image_path}") # Print path received

    if model is None:
        print("[classify_image] Model is not loaded. Returning error.")
        return "Model not loaded on server." # More user-friendly message

    # --- Detailed File Existence and Read Check (Using Pillow) ---
    print(f"[classify_image] Checking file existence at: {image_path}")
    if not os.path.exists(image_path):
        print("[classify_image] File DOES NOT exist at this moment.")
        return f"Error: File not found when classification function was called: {os.path.basename(image_path)}"
    print("[classify_image] File EXISTS. Attempting to read with Pillow...")

    img = None # Initialize img outside the try block
    try:
        # Attempt to read the image using Pillow
        # Removed time.sleep(0.1) before reading
        img = Image.open(image_path)
        print("[classify_image] Pillow Image.open operation finished.")

    except Exception as e:
        print(f"[classify_image] Exception caught during Image.open: {e}")
        import traceback
        traceback.print_exc()
        return f"Error during image reading (Pillow): {e}"

    # --- Check result of Image.open ---
    # Pillow's open doesn't return None like cv2.imread on failure, it raises an exception.
    # The exception is caught above.
    # We can still check if the object is valid, though usually not needed if no exception was raised.
    if img is None:
         # This case should ideally not be reached if Image.open raised an exception on failure
         print("[classify_image] Image.open returned None unexpectedly.")
         return "Error: Pillow Image.open returned None unexpectedly."

    print("[classify_image] Image read successfully by Pillow. Proceeding with preprocessing and prediction.")

    # --- Preprocessing and Prediction (Adapted for Pillow) ---
    try:
        # Resize the image to the model's expected input size (256x256)
        img = img.resize((256, 256))

        # Ensure image is in RGB format and convert to NumPy array
        # This is crucial for consistency with the model's expected input shape (256, 256, 3)
        img_array = np.array(img.convert('RGB'))

        # Normalize the image (assuming your training data was normalized by /255)
        img_array = img_array / 255.0

        # Add a batch dimension (model expects a batch of images)
        img_array = np.expand_dims(img_array, axis=0)

        # Make a prediction
        print("[classify_image] Attempting model prediction...")
        prediction = model.predict(img_array)
        print("[classify_image] Model prediction finished.")

        # Your notebook code used yhat > 0.5 for Happy
        # Assuming 0 represents sad and 1 represents happy
        if prediction[0][0] > 0.5:
            result = "Happy"
        else:
            result = "Sad"

        print(f"[classify_image] Prediction result: {result}")
        return result

    except Exception as e:
        print(f"[classify_image] Exception caught during preprocessing or prediction: {e}")
        import traceback # Print traceback for this exception
        traceback.print_exc()
        return f"Error during image processing: {e}"
