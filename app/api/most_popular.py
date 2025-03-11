from flask import Blueprint, jsonify
from app.database import db
from app.models.famous_place import FamousPlaces

mostpopular_api = Blueprint('mostpopular', __name__)

@mostpopular_api.route('/mostpopular', methods=['GET'])
def get_most_popular():
    try:
        # Fetch records from famous_places where most_popular is True
        popular_places = (
            db.session.query(FamousPlaces)
            .filter(FamousPlaces.most_popular == True)
            .all()
        )

        if not popular_places:
            return jsonify({"message": "No popular places found"}), 404

        # Prepare the list of records to return
        popular_places_data = [
            {
                "id": place.id,
                "image": place.image,
                "title": place.title,
                "location": place.location,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "video": place.video,
                "description": place.description,
                "most_popular": place.most_popular,
            }
            for place in popular_places
        ]

        # Return the data as JSON
        return jsonify({"most_popular": popular_places_data}), 200

    except Exception as e:
        print(f"Error fetching most popular places: {e}")
        return jsonify({"error": "An error occurred while fetching most popular places"}), 500
