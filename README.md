# Sensor Measurements Service

## Overview
This service stores sensor measurements into a PostgreSQL database via an HTTP REST API.

## Requirements
- Docker
- Docker Compose

## How to Run

1. **Build and start the service:**

```bash
docker-compose up --build
```

## Examples
1. **Example GET/POST valid bash commands**

    Commands to insert and retrieve values via API successfully (sensor_temperature must be included as parameter in Dockerfile)

    ```bash
    curl -X POST http://localhost:8080/api/v1/measurements/sensor_temperature -d '{"values":[{"time":1622548800,"value":25.3}]}'
    curl -X POST http://localhost:8080/api/v1/measurements/sensor_temperature -d '{"values":[{"time":1622548830,"value":26.3}]}'
    curl -X POST http://localhost:8080/api/v1/measurements/sensor_temperature -d '{"values":[{"time":1622548860,"value":23.3}]}'
    curl -X POST http://localhost:8080/api/v1/measurements/sensor_temperature -d '{"values":[{"time":1622548890,"value":24.3}]}'
    curl -X POST http://localhost:8080/api/v1/measurements/sensor_temperature -d '{"values":[{"time":1622548990,"value":34.3}]}'

    curl "http://localhost:8080/api/v1/measurements?measurement=sensor_temperature&from_time=1622548700&to_time=1622548900"
    ```

    Response
    ```bash
    {"sensor_temperature": [{"time": 1622548800, "value": 25.3}, {"time": 1622548830, "value": 26.3}, {"time": 1622548860, "value": 23.3}, {"time": 1622548890, "value": 24.3}, {"time": 1622548800, "value": 25.3}, {"time": 1622548830, "value": 26.3}, {"time": 1622548860, "value": 23.3}, {"time": 1622548890, "value": 24.3}]}
    ```

2. **Example GET/POST invalid bash commands**

    Example with unsupported measurement type (not included in Dockerfile)
    ```bash
    curl -X POST http://localhost:8080/api/v1/measurements/outdoor_temp -d '{"values":[{"time":1622548800,"value":25.3}]}'
    curl -X POST http://localhost:8080/api/v1/measurements/outdoor_temp -d '{"values":[{"time":1622548830,"value":26.3}]}'

    curl "http://localhost:8080/api/v1/measurements?measurement=outdoor_temp&from_time=1622548700&to_time=1622548900"
    ```

    Response
    ```bash
    Invalid measurement type
    Invalid measurement type
    Invalid measurement type: outdoor_temp
    ```
3. **Unit tests**
    - need to run db in docker container first
    ```bash
    docker-compose up --build
    ```
    - install requirements and run command in main directory
    ```bash
    pip install -r requirements.txt
    pytest tests/
    ```

    Coverage of unit tests
    ![alt text](<Screenshot 2024-08-07 at 13.13.58.png>)

4. **Performance test**
    Using python file `utils/perf_check_api.py` is possible to check performance of the POST requests. Test runs 10 1minute iterations using 100 concurrent requests