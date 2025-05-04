# # backend/auth.py

from flask import Blueprint, request, jsonify
from database import users_collection
from utils.encryption import encrypt_password, check_password
from utils.token import generate_token
import bson

auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     name = data['name']
#     email = data['email']
#     password = data['password']

#     if users_collection.find_one({"email": email}):
#         return jsonify({"error": "Email already exists"}), 400

#     hashed_password = encrypt_password(password)
#     users_collection.insert_one({
#         "name": name,
#         "email": email,
#         "password": hashed_password
#     })
#     return jsonify({"message": "User registered successfully"}), 201

# @auth_bp.route('/login', methods=['POST'])
# def login():
#     data = request.json
#     email = data['email']
#     password = data['password']
    

#     user = users_collection.find_one({"email": email})
#     if not user or not check_password(password, user['password']):
#         return jsonify({"error": "Invalid credentials"}), 401

#     token = generate_token(email)
#     return jsonify({"token": token}), 200

# new code 2
# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')
#     confirm_password = data.get('confirm_password')  # get the confirm password

#     # Check if password and confirm_password match
#     if password != confirm_password:
#         return jsonify({"error": "Passwords do not match"}), 400

#     if users_collection.find_one({"email": email}):
#         return jsonify({"error": "Email already exists"}), 400

#     hashed_password = encrypt_password(password)
#     users_collection.insert_one({
#         "name": name,
#         "email": email,
#         "password": hashed_password
#     })
#     return jsonify({"message": "User registered successfully"}), 201

# from flask import Blueprint, request, jsonify
# from database import users_collection
# from utils.encryption import encrypt_password, check_password
# from utils.token import generate_token
# import bson

# auth_bp = Blueprint('auth', __name__)

# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     print("Received data:", data)  # Debugging line to check incoming data

#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')
#     confirm_password = data.get('confirmPassword')  # Get the confirm password field

#     # Check if password and confirm_password match
#     if password != confirm_password:
#         return jsonify({"error": "Passwords do not match"}), 400

#     if users_collection.find_one({"email": email}):
#         return jsonify({"error": "Email already exists"}), 400

#     hashed_password = encrypt_password(password)
#     users_collection.insert_one({
#         "name": name,
#         "email": email,
#         "password": hashed_password
#     })
#     return jsonify({"message": "User registered successfully"}), 201
# auth.py

# backend/auth.py

from flask import Blueprint, request, jsonify
from database import users_collection
from utils.encryption import encrypt_password, check_password
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "YourJWTSecretKey"  # Change this to your own secret key

# Initialize Blueprint for authentication
auth_bp = Blueprint('auth', __name__)

# Route for user registration
# @auth_bp.route('/register', methods=['POST'])
# def register():
#     data = request.json
#     print("Register request received:", data)

#     # Extract form data
#     name = data.get('name')
#     email = data.get('email')
#     password = data.get('password')
#     confirm_password = data.get('confirmPassword')  # Important: confirmPassword with capital P!

#     # Validate passwords match
#     if password != confirm_password:
#         return jsonify({"error": "Passwords do not match"}), 400

#     # Check if email already exists
#     if users_collection.find_one({"email": email}):
#         return jsonify({"error": "Email already exists"}), 400

#     # Encrypt password and store user
#     hashed_password = encrypt_password(password)
#     users_collection.insert_one({
#         "name": name,
#         "email": email,
#         "password": hashed_password
#     })

#     return jsonify({"message": "User registered successfully"}), 201
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    print("Register request received:", data)

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirmPassword')

    if password != confirm_password:
        return jsonify({"error": "Passwords do not match"}), 400

    # Password strength validation
    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[!@$]).+$'
    if not re.match(password_pattern, password):
        return jsonify({
            "error": "Password must contain at least one lowercase letter, one uppercase letter, and one symbol (!, @, or $)"
        }), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = encrypt_password(password)
    users_collection.insert_one({
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201


# Route for user login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    print("Login request received:", data)

    # Ensure email and password are provided
    if not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    email = data.get('email')
    password = data.get('password')

    # Find the user
    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 400

    # Check password
    if not check_password(password, user['password']):
        return jsonify({"error": "Invalid email or password"}), 400

    # Generate JWT token
    payload = {
        "email": email,
        "exp": datetime.utcnow() + timedelta(days=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login successful", "token": token}), 200

from functools import wraps
from flask import request, jsonify
import jwt
from datetime import datetime

SECRET_KEY = "YourJWTSecretKey"

# Decorator to ensure the user is authenticated
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing or malformed"}), 403

        token = auth_header.split(" ")[1]  # Now safe

        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = decoded_token["email"]
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)
    
    return decorated_function
