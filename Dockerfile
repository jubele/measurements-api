FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py", "sensor_temperature", "battery_capacity"]
