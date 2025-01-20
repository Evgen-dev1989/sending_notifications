import requests
import asyncpg
from data import port, local_host, database, user, password
import asyncio

async def connect_db():

    try:
        conn = await asyncpg.connect(user=user, password=password, database=database, host=local_host, port=port)
        get_emails = await conn.fetch('SELECT email FROM users', 'value')
        return get_emails
    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        await conn.close()

async def main():
    
    url = "http://127.0.0.1:8000/notify/"

    base = connect_db()

    for i in base:

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