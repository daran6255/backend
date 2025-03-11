from flask import Blueprint, request, jsonify
from app.database import db
from app.models.famous_place import FamousPlaces

search_api = Blueprint('search', __name__)

@search_api.route('/search', methods=['GET'])
def search_places():
    try:
        # Get the search input from query parameters
        search_query = request.args.get('query', '').strip()

        if not search_query:
            return jsonify({"message": "Search query is required"}), 400

        # Perform a case-insensitive search in the title and description fields
        search_results = (
            db.session.query(FamousPlaces)
            .filter(
                (FamousPlaces.title.ilike(f"%{search_query}%")) | 
                (FamousPlaces.description.ilike(f"%{search_query}%"))
            )
            .all()
        )

        if not search_results:
            return jsonify({"message": "No matching places found"}), 404

        # Prepare the list of records to return
        search_results_data = [
            {
                "id": place.id,
                "image": place.image,
                "title": place.title,
                "location": place.location,
                "latitude": place.latitude,
                "longitude": place.longitude,
                "video": place.video,
                "description": place.description,
            }
            for place in search_results
        ]

        # Return the data as JSON
        return jsonify({"search_results": search_results_data}), 200

    except Exception as e:
        print(f"Error searching for places: {e}")
        return jsonify({"error": "An error occurred while searching for places"}), 500
