# backend/utils/mailer.py

from flask_mail import Mail, Message
import os

mail = Mail()  # initialize the Mail() object here

def send_output_email(app, to_email, output_path):
    msg = Message(
        subject="Lung Cancer Detection and Classification",
        sender=("Team RespAIration", "no-reply@yourdomain.com"),  
        recipients=[to_email]
    )
    msg.body = "Attached is your Grad-CAM result image based on your submitted CT scan."
    with app.open_resource(output_path) as fp:
        msg.attach(
            filename=os.path.basename(output_path),
            content_type="image/png",
            data=fp.read()
        )
    mail.send(msg)
