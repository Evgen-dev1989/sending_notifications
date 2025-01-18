import requests
import asyncpg
from data import port, local_host, database, user, password


url = "http://127.0.0.1:8000/notify/"
payload = {
    "recipient": "camkaenota1@gmail.com",
    "message": "Hello! This is a test email notification."
}
headers = {
    "Content-Type": "application/json"
}


async def command_execute(command, arguments = None):

    try:
        conn = await asyncpg.connect(user=user, password=password, database=database, host=local_host, port=port)
        if arguments is not None:
            print('HERE')
            await conn.execute(command, *arguments)
        else :
            await conn.execute(command)

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        await conn.close()

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(response.json())
