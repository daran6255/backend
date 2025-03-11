import os
import base64
import requests
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app.database import db
from app.models.famous_place import FamousPlaces

searchimage_api = Blueprint('searchimage', __name__)

def get_upload_folder():
    """Returns the correct upload folder path."""
    upload_folder = os.path.join(current_app.root_path, 'tmp')

    # Ensure the upload folder exists
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
        current_app.logger.debug(f"Image saved to {image_path}")

        # Convert the image to base64
        with open(image_path, "rb") as img_file:
            encoded_image = base64.b64encode(img_file.read()).decode('utf-8')

        current_app.logger.debug(f"Base64 Encoded Image: {encoded_image[:100]}...")  # Only show the first 100 characters

        # Call Google Vision API for image analysis
        google_vision_url = "https://vision.googleapis.com/v1/images:annotate"
        params = {
            'key': 'AIzaSyAgpLRt2kKWGB9gsTZqs92LO0_PJGKq1gg',  # Replace with your Google Vision API Key
        }

        # Prepare the request body with base64 image data
        body = {
            "requests": [
                {
                    "image": {
                        "content": encoded_image
                    },
                    "features": [
                        {
                            "type": "LABEL_DETECTION",
                            "maxResults": 1
                        }
                    ]
                }
            ]
        }

        # Send the image to the Vision API for analysis
        response = requests.post(google_vision_url, json=body, params=params)
        vision_data = response.json()

        current_app.logger.debug(f"Google Vision Response: {vision_data}")

        if 'responses' not in vision_data or not vision_data['responses']:
            return jsonify({"message": "No relevant results found from Vision API"}), 404

        # Get the label detected in the image
        detected_label = vision_data['responses'][0].get('labelAnnotations', [{}])[0].get('description', '')

        current_app.logger.debug(f"Detected label from Vision API: {detected_label}")

        # Search for the place in your database based on the detected label
        place = db.session.query(FamousPlaces).filter(FamousPlaces.title.ilike(f"%{detected_label}%")).first()

        if place:
            current_app.logger.debug(f"Place found in database: {place.title}")
        else:
            current_app.logger.debug("Place not found in the database")

        if not place:
            return jsonify({"message": "Place not found in the database"}), 404

        result_data = {
            "image": place.image,
            "title": place.title,
            "video": place.video,
            "description": place.description,
            "location": place.location
        }

        return jsonify(result_data), 200

    except Exception as e:
        current_app.logger.error(f"Error searching for places: {e}")
        return jsonify({"error": "An error occurred while processing the request"}), 500
