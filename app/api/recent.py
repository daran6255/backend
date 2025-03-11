from flask import Blueprint, request, jsonify
from app.database import db
from app.models.recent import Recent
from app.models.user import User
from app.models.famous_place import FamousPlaces

recent_api = Blueprint('recent_api', __name__)

@recent_api.route('/recent', methods=['GET'])
def get_recent():
    try:
        # Get user_id from query parameters
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400

        # Fetch the recent records for the given user_id
        recent_records = (
            db.session.query(Recent)
            .filter(Recent.user_id == user_id)
            .join(User, User.id == Recent.user_id)
            .join(FamousPlaces, FamousPlaces.id == Recent.famous_place_id)
            .all()
        )

        if not recent_records:
            return jsonify({"message": "No recent records found for this user"}), 404

        # Prepare the list of records to return
        recent_data = [
            {
                "user": {
                    "id": record.user.id,
                    "name": record.user.name,
                },
                "famous_place": {
                    "id": record.famous_place.id,
                    "image": record.famous_place.image,
                    "title": record.famous_place.title,
                    "location": record.famous_place.location,
                    "latitude": record.famous_place.latitude,
                    "longitude": record.famous_place.longitude,
                    "video": record.famous_place.video,
                    "description": record.famous_place.description,
                    "most_popular": record.famous_place.most_popular,
                },
                "searched_at": record.searched_at,
            }
            for record in recent_records
        ]

        # Return the recent data as JSON
        return jsonify({"recent": recent_data}), 200

    except Exception as e:
        print(f"Error fetching recent data: {e}")
        return jsonify({"error": "An error occurred while fetching recent data"}), 500
