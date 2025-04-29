# backend/app.py
from flask import Flask
from flask_cors import CORS
from auth import auth_bp
from predict import predict_bp
from utils.mailer import mail

app = Flask(__name__)

# Allow CORS for frontend
CORS(
    app,
    resources={
        r"/auth/*": {"origins": "http://localhost:3000"},
        r"/predict/*": {"origins": "http://localhost:3000"}
    },
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization"]
)

# SMTP Email Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'respairation@gmail.com'
app.config['MAIL_PASSWORD'] = 'gxil zmcj plys dhqc'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(predict_bp, url_prefix='/predict')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
