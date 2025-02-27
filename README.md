README

FastAPI + Celery + Redis + SMTP: Email Sending and CRUD via HTML Form

Description
This project is a web application built with FastAPI that implements:
- Email notifications using Celery and Redis.
- CRUD operations via an HTML form, allowing users to enter data.
- SMTP email sending using `smtplib`.
- Сompiled into a docker file.
  
Tech Stack
- **FastAPI** — asynchronous web framework.
- **Celery** — background task processing.
- **Redis** — task broker for Celery.
- **smtplib** — email sending via SMTP.
- **asyncpg** — asynchronous PostgreSQL database access.
- **httpx** — asynchronous HTTP requests.

Installation
1. Clone the repository:
https://github.com/Evgen-dev1989/sending_notifications.git

2. Install dependencies:
   pip install -r requirements.txt

3. Start Redis (if not already running):
   docker run -d -p 6379:6379 redis
   
5. Start Celery:
   celery -A tasks worker --loglevel=info --queues=notifications

6. Run the FastAPI server:
   uvicorn app:app --reload
   
Usage
- **Add data via the HTML form** — open your browser and navigate to `http://127.0.0.1:8000/notify/add_notify`.
- **Send emails** — once data is added, open your browser and navigate to `http://127.0.0.1:8000/notify/send_email`. Celery will process email sending in the background.

SMTP Configuration:
SMTP_SERVER=smtp.example.com
SMTP_PORT=587
SMTP_USER=your-email@example.com
SMTP_PASSWORD=yourpassword

Contact
If you have any questions, reach out to camkaenota@gmail.com.

License
This project is licensed under the MIT License.

