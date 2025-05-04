import os
import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_cors import CORS
from database import actions_collection
from inference import predict_image
from gradcam import generate_gradcam
from utils.mailer import send_output_email
from auth import token_required  # Import the token_required decorator

predict_bp = Blueprint('predict', __name__)

# CORS enabled for this blueprint
CORS(predict_bp, origins="http://localhost:3000", supports_credentials=True)

UPLOAD_FOLDER = 'static/input_images'
OUTPUT_FOLDER = 'static/output_images'

@predict_bp.route('/predict', methods=['POST'])
def predict():
    doctor_name = request.form['doctor_name']
    hospital_name = request.form['hospital_name']
    email = request.form['email']
    image = request.files['image']

    # Ensure upload directories exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Save the uploaded image
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{image.filename}"
    input_path = os.path.join(UPLOAD_FOLDER, filename)
    image.save(input_path)

    # Run prediction
    predicted_class = predict_image(input_path)

    # Generate GradCAM output
    output_filename = f"{timestamp}_gradcam.png"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)
    generate_gradcam(input_path, output_path)

    # Save record to MongoDB
    actions_collection.insert_one({
        "user_email": email,
        "doctor_name": doctor_name,
        "hospital_name": hospital_name,
        "input_image_path": input_path,
        "output_image_path": output_path,
        "date": datetime.datetime.utcnow()
    })

    # Send output email
    send_output_email(current_app, email, output_path)

    # Respond
    return jsonify({
        "message": "Prediction successful",
        "predicted_class": predicted_class,
        "input_image_url": input_path,
        "output_image_url": output_path
    }), 200

# Updated previous-actions route with token validation
@predict_bp.route('/previous-actions', methods=['GET'])
@token_required  # Use the token_required decorator for this route
def previous_actions(current_user):  # current_user is the email extracted from the token
    # Use the current_user to filter actions by email
    actions = actions_collection.find({"user_email": current_user})
    response = []

    for action in actions:
        response.append({
            "date": action["date"],
            "doctor_name": action["doctor_name"],
            "input_image_path": action["input_image_path"],
            'hospital_name': action["hospital_name"],
            "output_image_path": action["output_image_path"]
        })

    return jsonify(response), 200
