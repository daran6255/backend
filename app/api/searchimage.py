import requests
import base64
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.database import db
from app.models.famous_place import FamousPlaces

searchimage_api = Blueprint('searchimage', __name__)

# Google API keys and Search Engine ID
GOOGLE_VISION_API_KEY = "AIzaSyAgpLRt2kKWGB9gsTZqs92LO0_PJGKq1gg"  # Your Google Vision API Key

def get_upload_folder():
    """Returns the correct upload folder path."""
    upload_folder = os.path.join(current_app.root_path, 'tmp')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    return upload_folder

@searchimage_api.route('/searchimage', methods=['POST'])
def search_places():
    try:
        # Get the image from the request
        image_file = request.files.get('image')
        filename = secure_filename(image_file.filename)
        upload_folder = get_upload_folder()
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)

        # Convert image to base64 for Vision API
        with open(image_path, 'rb') as img:
            image_data = img.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Prepare payload for Google Vision API with Landmark Detection
        payload = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "LANDMARK_DETECTION"  # Use LANDMARK_DETECTION for landmark identification
                        }
                    ]
                }
            ]
        }

        # Make a request to Google Vision API
        vision_api_url = f"https://vision.googleapis.com/v1/images:annotate?key={GOOGLE_VISION_API_KEY}"
        response = requests.post(vision_api_url, json=payload)

        # Handle Vision API response
        vision_response = response.json()
        if "responses" in vision_response:
            landmarks = vision_response["responses"][0].get("landmarkAnnotations", [])
            if landmarks:
                # Extract the most relevant landmark description
                landmark_description = landmarks[0].get("description")
                current_app.logger.debug(f"Detected landmark: {landmark_description}")

                # Search for the landmark in the FamousPlaces table
                place = db.session.query(FamousPlaces).filter(FamousPlaces.title.ilike(f"%{landmark_description}%")).first()

                if place:
                    result_data = {
                        "image": place.image,
                        "title": place.title,
                        "video": place.video,
                        "description": place.description,
                        "location": place.location
                    }
                    print(result_data)
                    return jsonify(result_data), 200
                else:
                    current_app.logger.debug(f"Place '{landmark_description}' not found in the database.")
                    return jsonify({"message": f"Place '{landmark_description}' not found in the database."}), 404
            else:
                current_app.logger.debug("No landmarks detected in the image.")
                return jsonify({"message": "No landmarks detected in the image."}), 404
        else:
            current_app.logger.debug("Error in Vision API response.")
            return jsonify({"message": "Error in Vision API response."}), 500

    except Exception as e:
        current_app.logger.error(f"Error searching for places: {e}")
        return jsonify({"error": "An error occurred while processing the request."}), 500
