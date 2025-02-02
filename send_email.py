import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import Config


def send_notification(email: str, message: str):
    if email is None or not email:
            return {"status": "error", "message": "Recipient email is required"}
    try:
        mime_part = MIMEMultipart()
        mime_part["From"] = Config.user_email
        mime_part["To"] = email
        mime_part["Subject"] = "Notification"
        
        mime_part.attach(MIMEText(message, "plain"))
        
        with smtplib.SMTP(Config.host, Config.port) as server:
            server.starttls()
            server.login(Config.user_email, Config.password_email)
            server.sendmail(Config.user_email, email, mime_part.as_string())
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

