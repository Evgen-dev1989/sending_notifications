FROM python:3.9-slim
WORKDIR /main
COPY . .
RUN pip install -r requirements.txt
ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "start.py"]