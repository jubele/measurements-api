import aiohttp
import asyncio
import time
import random

# Constants
BASE_URL = 'http://localhost:8080/api/v1/measurements/sensor_temperature'
CONCURRENT_REQUESTS = 100
TEST_DURATION = 60
ITERATIONS = 10

async def post_measurement(session, url):
    measurement = {
        "values": [
            {"time": int(time.time()), "value": random.uniform(20.0, 30.0)}
        ]
    }
    async with session.post(url, json=measurement) as response:
        if response.status != 204:
            print(f"Request failed with status code: {response.status}")

async def run_benchmark():
    async with aiohttp.ClientSession() as session:
        start_time = time.time()
        end_time = start_time + TEST_DURATION
        total_requests = 0

        while time.time() < end_time:
            tasks = []
            for _ in range(CONCURRENT_REQUESTS):
                task = asyncio.ensure_future(post_measurement(session, BASE_URL))
                tasks.append(task)

            await asyncio.gather(*tasks)
            total_requests += CONCURRENT_REQUESTS

        return total_requests

def main():
    successfull_requests = []
    for i in range(ITERATIONS):
        print(f"Benchmarking... {i+1}/{ITERATIONS}")
        loop = asyncio.get_event_loop()
        total_requests = loop.run_until_complete(run_benchmark())
        successfull_requests.append(total_requests)
    print(f"Results of requests per minute\n\
        Average: {sum(successfull_requests)/len(successfull_requests)}\n\
        Min: {min(successfull_requests)}\nMax:{max(successfull_requests)}")

if __name__ == '__main__':
    main()
