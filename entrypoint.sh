!/bin/bash
docker run -d -p 6379:6379 redis

celery -A tasks worker --loglevel=info --queues=notifications &

uvicorn app:app --reload