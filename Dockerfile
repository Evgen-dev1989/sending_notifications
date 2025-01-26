FROM python:3.9-slim
WORKDIR /sending_notifications
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "start.py"]
