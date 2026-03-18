from flask import Flask, render_template, request        #python -m flask --app email_app run
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request
from flask_cors import CORS   # add this

from dotenv import load_dotenv
import os

load_dotenv()   # load .env file

GMAIL_ID = os.getenv("GMAIL_ID")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

app = Flask(__name__)
CORS(app)   # enable CORS

@app.route("/", methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        cc = request.form["cc"]

        msg = EmailMessage()
        msg["Subject"] = "Submission of Form 11 EPF Declaration"
        msg["From"] = GMAIL_ID
        msg["To"] = email
        msg["CC"] = cc
        msg.set_content(
            f"""Dear {name},

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

        # Attach PDF
        with open("EPFO Form11.pdf", "rb") as pdf:
            msg.add_attachment(
                pdf.read(),
                maintype="application",
                subtype="pdf",
                filename="Document.pdf"
            )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ID, GMAIL_APP_PASSWORD)
            server.send_message(msg)

        return "✅ Email sent successfully!"

    return render_template("index.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

