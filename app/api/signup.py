from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from ..models.user import User
from ..database import db

signup_api = Blueprint('signup', __name__)

@signup_api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    required_fields = ['name', 'dob', 'email', 'password', 'confirmPassword', 'gender', 'differently_abled']
    if not all(field in data for field in required_fields):
        return jsonify({'detail': 'Missing required fields'}), 400

    if data['password'] != data['confirmPassword']:
        return jsonify({'detail': 'Passwords do not match'}), 400

    try:
        dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'detail': 'Invalid date format for dob. Please use YYYY-MM-DD.'}), 400

    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'detail': 'Email already in use'}), 400

    if data['gender'] == 'Male':
        avatar_url = 'https://winvinayafoundation.org/wp-content/uploads/2024/12/male_user_avatar.png'
    elif data['gender'] == 'Female':
        avatar_url = 'https://winvinayafoundation.org/wp-content/uploads/2024/12/female_user_avatar.png'
    else:
        avatar_url = ''

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(
        name=data['name'],
        dob=dob,
        email=data['email'],
        password=hashed_password,
        gender=data['gender'],
        differently_abled=data['differently_abled'],
        avatar=avatar_url
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'detail': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'detail': 'An error occurred while creating the user', 'error': str(e)}), 500
