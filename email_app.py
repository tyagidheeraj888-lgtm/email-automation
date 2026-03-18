from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

GMAIL_ID = os.getenv("GMAIL_ID")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/send-email", methods=["POST"])
def send_email():

    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        cc = data.get("cc")
    else:
        name = request.form["name"]
        email = request.form["email"]
        cc = request.form["cc"]

    msg = EmailMessage()
    msg["Subject"] = "Submission of Form 11 EPF Declaration"
    msg["From"] = GMAIL_ID
    msg["To"] = email
    msg["CC"] = cc
    msg.set_content(f"Dear {name}, please find attached document.")

    with open("EPFO Form11.pdf", "rb") as pdf:
        msg.add_attachment(pdf.read(), maintype="application", subtype="pdf", filename="Document.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(GMAIL_ID, GMAIL_APP_PASSWORD)
        server.send_message(msg)

    return jsonify({"message": "Email sent successfully"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)