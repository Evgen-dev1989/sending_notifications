import asyncio
from typing import Optional

import asyncpg
import httpx
from fastapi import HTTPException

from data import database, local_host, local_port, password, user

create_db = [
    # """
    # DROP TABLE IF EXISTS api CASCADE;
    # """,
    """
    CREATE TABLE IF NOT EXISTS api (
    id SERIAL PRIMARY KEY,
    time TIMESTAMP DEFAULT NOW(),
    email VARCHAR(250) NOT NULL,
    message VARCHAR(250));
        """]

test = "INSERT INTO api (email, message) VALUES ('test@gmail.com', 'Hi! We will be glad to see you at our party.')"


async def command_execute(commands):
    conn = None
    try:
        conn = await asyncpg.connect(user=user, password=password, database=database, host='localhost', port=local_port)

        if isinstance(commands, (list, tuple)):
            for command in commands:
                await conn.execute(command)
        else:
            await conn.execute(commands)

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        if conn:
            await conn.close()


async def connect_db():
    return await asyncpg.connect(user=user, password=password, database=database, host=local_host, port=local_port)

async def get_all():
 
    conn = None
    try:
        conn = await connect_db()
        records = await conn.fetch('SELECT id, email, message FROM api')
        return records

    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if conn is not None:  
            await conn.close()


async def get_by_id(id: int):
    conn = None
    try:
        conn = await connect_db()
        record = await conn.fetchrow('SELECT id, email, message FROM api WHERE id = $1', id)
        if record:
            return {"id": record["id"], "email": record["email"], "message": record["message"]}
        else:
            raise HTTPException(status_code=404, detail="Not found")
        
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if conn is not None:  
            await conn.close()


async def add_notify(email: Optional[str], message: Optional[str]):

    try:
        conn = await connect_db()
        new = await conn.fetchval(
            'INSERT INTO api (email, message) VALUES ($1, $2) RETURNING id',
                email, message
            )
        return {"id": new, "email": email, "message": message}
    
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    finally:
        if conn is not None:  
            await conn.close()


async def update_notify(id: int, email: Optional[str], message: Optional[str]):

    try:
        conn = await connect_db()
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
    
    except asyncpg.PostgresError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if conn is not None:  
            await conn.close()




async def del_notify(id: int):
    try:
        conn = await connect_db()
        result = await conn.execute('DELETE FROM api WHERE id = $1', id)
        deleted_rows = int(result.split("DELETE ")[-1])

        if deleted_rows == 0:
            raise HTTPException(status_code=404, detail=f"Notify with id {id} not found")
        
    except HTTPException as e:
        raise e 
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if conn is not None:  
            await conn.close()


async def main():
    await command_execute(create_db)

    await command_execute(test)

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

