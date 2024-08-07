import pytest
from aiohttp.test_utils import AioHTTPTestCase
import os
import logging

os.environ['PG_USER'] = 'testuser'
os.environ['PG_PWD'] = 'testpassword'

from app import init_app

logging.basicConfig(level=logging.INFO)

class SensorMeasurementsTestCase(AioHTTPTestCase):

    async def get_application(self):
        logging.info('init')
        return await init_app(['temperature'])

    async def test_post_measurement(self):
        resp = await self.client.post('/api/v1/measurements/temperature', json={
            "values": [{"time": 1622548800, "value": 25.3}]
        })
        assert resp.status == 204

    async def test_get_measurements(self):
        await self.client.post('/api/v1/measurements/temperature', json={
            "values": [{"tme": 1622548800, "value": 25.3}]
        })
        resp = await self.client.get('/api/v1/measurements', params={
            'measurement': 'temperature',
            'from_time': 1622548700,
            'to_time': 1622548900
        })
        assert resp.status == 200
        data = await resp.json()
        assert 'temperature' in data

    async def test_post_measurement_invalid_measurement(self):
        resp = await self.client.post('/api/v1/measurements/temperature_invalid', json={
            "values": [{"time": 1622548800, "value": 25.3}]
        })
        assert resp.status == 400

    async def test_get_measurement_invalid_measurement(self):
        resp = await self.client.get('/api/v1/measurements', params={
            'measurement': 'temperature_invalid',
            'from_time': 1622548700,
            'to_time': 1622548900
        })
        assert resp.status == 400
