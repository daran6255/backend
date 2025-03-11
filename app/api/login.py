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
        print("Login API called")  # Debugging
        
        # Parse JSON data from request
        data = request.get_json()
        print(f"Received Data: {data}")  # Debugging
        
        email = data.get('email')
        password = data.get('password')

        # Validate input
        if not email or not password:
            print("Missing email or password")  # Debugging
            return jsonify({"error": "Email and password are required"}), 400

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        print(f"User found: {user}")  # Debugging
        
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
        print(f"Generated Token: {token}")  # Debugging

        # Return user data
        user_data = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "dob": user.dob,
            "gender": user.gender,
            "differently_abled": user.differently_abled,
            "avatar": user.avatar
        }
        print(f"User Data: {user_data}")  # Debugging
        
        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": user_data
        }), 200

    except Exception as e:
        print(f"Error during login: {e}")  # Debugging
        return jsonify({"error": "An error occurred during login"}), 500
