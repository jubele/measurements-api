import sys
from aiohttp import web
from api import setup_routes
from db import init_db, close_db
import logging

logging.basicConfig(level=logging.DEBUG)

async def init_app(measurement_types):
    app = web.Application()
    app['measurement_types'] = set(measurement_types)
    setup_routes(app)
    app.on_startup.append(init_db)
    app.on_cleanup.append(close_db)
    return app

def main():
    provided_types = sys.argv[1:]
    if not provided_types:
        logging.error("No measurement types provided. Exiting.")
        sys.exit(1)

    logging.info(f"Starting service with measurement types: {provided_types}")
    
    app = init_app(provided_types)
    web.run_app(app, port=8080)
    print()

if __name__ == '__main__':
    main()
