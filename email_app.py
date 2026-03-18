from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
import threading

# Load environment variables
load_dotenv()

GMAIL_ID = os.getenv("GMAIL_ID")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

app = Flask(__name__)
CORS(app)


# ------------------ HOME ROUTE ------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# ------------------ EMAIL FUNCTION (ASYNC) ------------------
def send_mail_async(msg):
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(GMAIL_ID, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("✅ Email sent successfully")

    except Exception as e:
        print("❌ Email error:", str(e))


# ------------------ API ROUTE ------------------
@app.route("/send-email", methods=["POST"])
def send_email():

    # Support both JSON and form data
    if request.is_json:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        cc = data.get("cc")
    else:
        name = request.form.get("name")
        email = request.form.get("email")
        cc = request.form.get("cc")

    # Create email
    msg = EmailMessage()
    msg["Subject"] = "Submission of Form 11 EPF Declaration"
    msg["From"] = GMAIL_ID
    msg["To"] = email
    msg["CC"] = cc

    msg.set_content(f"""Dear {name},

As part of the onboarding and statutory compliance process, all new employees are required to fill and submit Form 11 (EPF Declaration Form) in accordance with the guidelines of the Employees’ Provident Fund Organisation (EPFO).

Form 11 is mandatory to declare your previous employment and EPF membership details, if any, and is essential for the processing of your EPF records.

Kindly ensure that:
- The form is filled accurately and completely
- All required sections are duly signed
- The completed form is submitted to the HR & Admin Department

Note- If you are enrolling for the first time, kindly register on the UMANG app and share your UAN number with us.

Please note that failure to submit Form 11 or submission of incorrect information may result in delays in EPF registration and related benefits.

For any assistance or clarification, please reach out to the HR & Admin Department.

Regards,  
Dheeraj Kumar  
Accounts & Admin
XTEN-AV India Pvt Ltd.  
Mob: 8588058784  
Noida One Business Park  
Tower B-511 to 513, Sector 62, Noida-201309  
www.xtenav.com
"""
)
    # Attach PDF (if exists)
    file_path = "EPFO Form11.pdf"
    if os.path.exists(file_path):
        with open(file_path, "rb") as pdf:
            msg.add_attachment(
                pdf.read(),
                maintype="application",
                subtype="pdf",
                filename="Form11.pdf"
            )
    else:
        print("⚠️ PDF file not found")

    # Send email in background (prevents timeout)
    threading.Thread(target=send_mail_async, args=(msg,)).start()

    return jsonify({"message": "Email is being sent"})


# ------------------ RUN APP ------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)