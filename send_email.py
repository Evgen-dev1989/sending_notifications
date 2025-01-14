import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config

def email(recipient: str, message: str):
    if not recipient:
            return {"status": "error", "message": "Recipient email is required"}
    try:
        mime_part = MIMEMultipart()
        mime_part["From"] = Config.user_email
        mime_part["To"] = recipient
        mime_part["Subject"] = "Notification"
        
        mime_part.attach(MIMEText(message, "plain"))
        
        with smtplib.SMTP(Config.host, Config.port) as server:
            server.starttls()
            server.login(Config.user_email, Config.password_email)
            server.sendmail(Config.user_email, recipient, mime_part.as_string())
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    

