from flask import Blueprint, request, jsonify
import requests

location_api = Blueprint('location_api', __name__)

# Replace with your geocoding API key
GEOCODING_API_KEY = "AIzaSyD42S9jNyAP0nijNRni0lQuhTx7UkNLTGA"

@location_api.route('/get-location', methods=['POST'])
def get_location():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Validate the input
        if not latitude or not longitude:
            return jsonify({"error": "Latitude and longitude are required"}), 400

        # Call the geocoding API to fetch city details
        response = requests.get(
            f"https://maps.googleapis.com/maps/api/geocode/json?latlng={latitude},{longitude}&key={GEOCODING_API_KEY}"
        )
        if response.status_code != 200:
            return jsonify({"error": "Failed to fetch location details"}), 500

        location_data = response.json()
        if "results" in location_data and location_data["results"]:
            # Extract city name from the results
            for component in location_data["results"][0]["address_components"]:
                if "locality" in component["types"]:
                    city = component["long_name"]
                    print(city)
                    return jsonify({"city": city}), 200

        return jsonify({"error": "City not found for the provided coordinates"}), 404

    except Exception as e:
        print(f"Error while fetching location: {e}")
        return jsonify({"error": "An error occurred while fetching the location"}), 500
