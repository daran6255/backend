from flask import Blueprint, request, jsonify
from app.database import db
from app.models.famous_place import FamousPlaces
from geopy.geocoders import Nominatim

search_location_api = Blueprint('search_location', __name__)

@search_location_api.route('/search_location', methods=['POST'])
def search_location():
    try:
        # Parse latitude and longitude from the request
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and longitude are required"}), 400

        # Use geopy to get city and state based on latitude and longitude
        geolocator = Nominatim(user_agent="geoapi")
        location = geolocator.reverse(f"{latitude}, {longitude}")

        if not location or not location.raw.get('address'):
            return jsonify({"error": "Unable to determine location"}), 404

        address = location.raw['address']
        city = address.get('city', address.get('town', address.get('village', 'Unknown')))
        state = address.get('state', 'Unknown')

        # Query the famous_places table to find matching records
        matching_places = (
            db.session.query(FamousPlaces)
            .filter(FamousPlaces.location.ilike(f"%{city}%") | FamousPlaces.location.ilike(f"%{state}%"))
            .all()
        )

        if not matching_places:
            return jsonify({"message": "No places found for the given location"}), 404

        # Prepare the response data
        places_data = [
            {
                "id": place.id,
                "image": place.image,
                "title": place.title,
                "video": place.video,
                "description": place.description,
                "location": place.location,
            }
            for place in matching_places
        ]

        # Return the data as JSON
        return jsonify({"places": places_data}), 200

    except Exception as e:
        print(f"Error in search_location API: {e}")
        return jsonify({"error": "An error occurred while processing the location data"}), 500
