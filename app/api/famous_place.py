from flask import Blueprint, request, jsonify
from app.database import db
from app.models.famous_place import FamousPlaces  # Import the FamousPlaces model

geo_api = Blueprint('geo_api', __name__)

@geo_api.route('/famousplaces/nearby', methods=['GET'])
def get_nearby_locations():
    try:
        # Extract latitude and longitude from request arguments
        latitude = request.args.get('latitude', type=float)
        longitude = request.args.get('longitude', type=float)
        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and Longitude are required"}), 400

        # Define a threshold distance in degrees (example: ~10 km)
        threshold_distance = 0.1  # Adjust as needed

        # Query the database for locations within the threshold distance
        records = FamousPlaces.query.filter(
            (FamousPlaces.latitude >= latitude - threshold_distance) &
            (FamousPlaces.latitude <= latitude + threshold_distance) &
            (FamousPlaces.longitude >= longitude - threshold_distance) &
            (FamousPlaces.longitude <= longitude + threshold_distance)
        ).all()

        if not records:
            return jsonify({"message": "No nearby locations found"}), 404

        # Format the data to include image, title, location, latitude, longitude, video, and description
        data = [
            {
                "image": record.image,
                "title": record.title,
                "location": record.location,
                "latitude": record.latitude,
                "longitude": record.longitude,
                "video": record.video,
                "description": record.description
            }
            for record in records
        ]

        return jsonify({"nearby_locations": data}), 200
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An error occurred"}), 500
