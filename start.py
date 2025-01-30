import requests
import asyncpg
from data import local_host, database, user, password, local_port
import asyncio

async def connect_db():
 
    conn = None
    try:
        conn = await asyncpg.connect(user=user, password=password, database=database, host=local_host, port=local_port)
        get_emails = await conn.fetch('SELECT email FROM api')
        get_emails = await conn.fetch('SELECT email FROM api')
        return get_emails
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        if conn:
            await conn.close()

async def main():

    url = "http://127.0.0.1:8000/notify/send_all"

    base = await connect_db()

    emails = [record['email'] for record in base]

    for i in emails:
        payload = {
        "recipient": i,
        "message": "Hi! We'll be glad to see you at our party."
        }
        
        headers = {
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code)
        print(response.json())

if __name__ == '__main__':
    asyncio.run(main())

#uvicorn app:app --reload
#docker run -d -p 6379:6379 redis
#celery -A tasks worker --loglevel=info --queues=notifications