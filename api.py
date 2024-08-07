from aiohttp import web
import json
from db import save_measurements, get_measurements

async def handle_post_measurement(request):
    measurement_type = request.match_info['measurement_type']
    if measurement_type not in request.app['measurement_types']:
        return web.Response(status=400, text="Invalid measurement type")
    
    try:
        data = await request.json()
        await save_measurements(request.app, measurement_type, data['values'])
        return web.Response(status=204)
    except (KeyError, json.JSONDecodeError):
        return web.Response(status=400)

async def handle_get_measurements(request):
    try:
        measurement_types = request.query.getall('measurement')
        for measurement_type in measurement_types:
            if measurement_type not in request.app['measurement_types']:
                return web.Response(status=400, text=f"Invalid measurement type: {measurement_type}")
        
        from_time = int(request.query['from_time'])
        to_time = int(request.query['to_time'])
        result = await get_measurements(request.app, measurement_types, from_time, to_time)
        return web.json_response(result)
    except (KeyError, ValueError):
        return web.Response(status=400)

def setup_routes(app):
    app.router.add_post('/api/v1/measurements/{measurement_type}', handle_post_measurement)
    app.router.add_get('/api/v1/measurements', handle_get_measurements)
