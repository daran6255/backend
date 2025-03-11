import os
import tempfile
from flask import Blueprint, request, jsonify, current_app
from app.database import db
from app.models.famous_place import FamousPlaces
from werkzeug.utils import secure_filename
import requests
from PIL import Image
import io
import base64

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
        # Get the image, latitude, and longitude from the request
        image_file = request.files.get('image')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')

        if not image_file or not latitude or not longitude:
            return jsonify({"message": "Image, latitude, and longitude are required"}), 400
        
        # Secure the image filename and save it temporarily in the correct folder
        filename = secure_filename(image_file.filename)

        # Get the upload folder dynamically and ensure it's created
        upload_folder = get_upload_folder()

        # Create the path to save the image
        image_path = os.path.join(upload_folder, filename)

        # Save the image to the temporary file path
        image_file.save(image_path)
        
        # Log the saved file path for debugging
        current_app.logger.debug(f"Image saved to {image_path}")

        # Convert image to base64 (optional: depending on the Google API you are using)
        # This assumes you want to encode the image to base64 for direct search
        with open(image_path, 'rb') as img:
            image_data = img.read()
            encoded_image = base64.b64encode(image_data).decode('utf-8')

        # Log image data for debugging (optional)
        current_app.logger.debug(f"Base64 Encoded Image: {encoded_image[:100]}...")  # Only show the first 100 characters for safety

        # Call Google Search API to search for places using the image
        google_search_url = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': 'AIzaSyDMR8DxlYeDaJXSDeMJeL0Bw4cg4X3b9r4',  # Replace with your Google API key
            'cx': 'c74e41907a14c4ace',  # Replace with your Custom Search Engine ID
            'searchType': 'image',  # Ensure it's an image search
            'fileType': 'jpg'  # You can adjust this to match the file type you're using
        }
        response = requests.get(google_search_url, params=params)
        search_data = response.json()

        # Log the search response for debugging
        current_app.logger.debug(f"Google Search Response: {search_data}")

        if 'items' not in search_data or not search_data['items']:
            return jsonify({"message": "No relevant results found from Google Search"}), 404
        
        # Get the name from Google search results
        place_name = search_data['items'][0]['title']
        
        # Log the place name extracted from the search result
        current_app.logger.debug(f"Place name from Google Search: {place_name}")

        # Search the FamousPlaces table for the place name
        place = db.session.query(FamousPlaces).filter(FamousPlaces.title.ilike(f"%{place_name}%")).first()

        # Log the result of the database query
        if place:
            current_app.logger.debug(f"Place found in database: {place.title}")
        else:
            current_app.logger.debug("Place not found in the database")

        if not place:
            return jsonify({"message": "Place not found in the database"}), 404

        # Prepare the result data
        result_data = {
            "image": place.image,
            "title": place.title,
            "video": place.video,
            "description": place.description,
            "location": place.location
        }

        return jsonify(result_data), 200

    except Exception as e:
        # Log the error to understand the issue better
        current_app.logger.error(f"Error searching for places: {e}")
        return jsonify({"error": "An error occurred while processing the request"}), 500
