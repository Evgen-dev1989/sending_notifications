import asyncio

import asyncpg

from fastapi import HTTPException
import httpx
from celery import Celery
import asyncpg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



from data import database, local_host, local_port, password, user
from base_model import Model




async def connect_db():
    return await asyncpg.connect(user=user, password=password, database=database, host=local_host, port=local_port)

async def get_all():
 
    conn = None
    try:
        conn = await connect_db()
        records = await conn.fetch('SELECT id, email, message FROM api')
        return records

    except Exception as e:
        print(f"Error: {e}")
        raise 

    finally:
        if conn:
            await conn.close()


async def get_by_id(email_id: int):
    
    conn = await connect_db()
    try:
        record = await conn.fetchrow('SELECT id, email, message FROM api WHERE id = $1', email_id)
        if record:
            return {"id": record["id"], "email": record["email"], "message": record["message"]}
        else:
            raise HTTPException(status_code=404, detail="Message not found")

    finally:
        if conn:
            await conn.close()


async def add_notify(email: Model, message: Model):

    conn = await connect_db()
    try:
        new = await conn.fetchval(
            'INSERT INTO api (email, message) VALUES ($1, $2) RETURNING id',
                email, message
            )
        return {"id": new, "email": email, "message": message}
    
    except Exception as e:
        print(f"Error: {e}")
        raise 

    finally:
        if conn:
            await conn.close()


async def update_notify(id: Model, email: Model, message: Model):

    conn = await connect_db()
    try:
        record = await conn.fetchrow('SELECT * FROM api WHERE id = $1', id)
        if not record:
            raise HTTPException(status_code=404, detail="Message not found")

        updated_email = email if email else record["email"]
        updated_message = message if message else record["message"]

        await conn.execute(
            'UPDATE api SET email = $1, message = $2 WHERE id = $3',
            updated_email, updated_message, id
        )
        return {"id": id, "email": updated_email, "message": updated_message}
    
    finally:
        if conn:
            await conn.close()



async def del_notify(id: int):
    conn = await connect_db()
    try:
        result = await conn.execute('DELETE FROM api WHERE id = $1', id)
        deleted_rows = int(result.split("DELETE ")[-1])
        return {"message": f"Message with id {id} deleted successfully"}
    
    except:
        raise HTTPException(status_code=404, detail="Message not found")
    finally:
        await conn.close()



async def main():

    base = await get_all()

    url = "http://127.0.0.1:8000/notify/send_email"
    headers = {"Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        tasks = []
        for record in base:
            payload = {"id": record["id"], "email": record["email"], "message": record["message"]}
            tasks.append(client.post(url, json=payload, headers=headers))

        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response.status_code, response.json())
    
if __name__ == '__main__':
    asyncio.run(main())

#uvicorn app:app --reload
#docker run -d -p 6379:6379 redis
#celery -A tasks worker --loglevel=info --queues=notifications

