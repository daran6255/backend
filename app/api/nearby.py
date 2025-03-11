from flask import Blueprint, jsonify, request
from app.database import db
from app.models.famous_place import FamousPlaces

nearby_api = Blueprint('nearby', __name__)

@nearby_api.route('/nearby', methods=['POST'])
def get_nearby():
    try:
        # Fetch the city name from the request JSON body
        data = request.get_json()
        city_name = data.get('city')

        if not city_name:
            return jsonify({"error": "City name is required"}), 400

        # Use the city_name to query nearby famous places
        nearby_places = (
            db.session.query(FamousPlaces)
            .filter(FamousPlaces.location.ilike(f"%{city_name}%"))  # Filter places based on city name
            .all()
        )

        if not nearby_places:
            return jsonify({"message": "No nearby places found"}), 404

        # Prepare the places data to return
        places_data = [
            {
                "id": place.id,
                "image": place.image,
                "title": place.title,
                "location": place.location,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "video": place.video,
                "description": place.description
            }
            for place in nearby_places
        ]

        return jsonify({"nearby_famous_places": places_data}), 200

    except Exception as e:
        # Handle any other exceptions
        print(f"Error fetching nearby places: {e}")
        return jsonify({"error": "An error occurred while fetching nearby places"}), 500
