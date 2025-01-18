import requests

url = "http://127.0.0.1:8000/notify/"
payload = {
    "recipient": "camkaenota1@gmail.com",
    "message": "Hello! This is a test email notification."
}
headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
