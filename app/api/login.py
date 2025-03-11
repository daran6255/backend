from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from app.database import db
from app.models.user import User
import jwt
import datetime

login_api = Blueprint('login_api', __name__)

# Load the secret key from the app config
def get_secret_key():
    from app.config import Config
    return Config.SECRET_KEY

@login_api.route('/login', methods=['POST'])
def login():
    try:
        # Parse JSON data from request
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Invalid email or password"}), 401

        # Verify password
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid email or password"}), 401

        # Generate JWT token
        token = jwt.encode(
            {
                "user_id": user.id,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            get_secret_key(),
            algorithm="HS256"
        )
        # print(token)

        # Return all user fields in the response
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "dob": user.dob,
            "gender": user.gender,
            "differently_abled": user.differently_abled,
            "avatar": user.avatar
        }
        # print(user_data)
        return jsonify({
            "message": "Login successful",      
            "token": token,
            "user": user_data
        }), 200

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "An error occurred during login"}), 500