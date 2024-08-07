import os
import asyncpg
import asyncio
import logging

MAX_RETRIES = 5
RETRY_DELAY = 5

DB_HOST = os.getenv('DB_HOST', 'db')

async def init_db(app):
    retries = 0
    PG_USER = os.getenv('PG_USER')
    PG_PWD = os.getenv('PG_PWD')
    while retries < MAX_RETRIES:
        try:
            logging.info(f'Connecting db ...')
            app['db'] = await asyncpg.create_pool(dsn=f'postgresql://{PG_USER}:{PG_PWD}@{DB_HOST}/sensor_db',
                                                  min_size=1,
                                                  max_size=20)
            logging.info("Connected to the database successfully.")
            await init_schema(app)
            break
        except (asyncpg.exceptions.ConnectionDoesNotExistError, OSError, Exception) as e:
            retries += 1
            logging.warning(f"Database connection failed. Retry {retries}/{MAX_RETRIES} in {RETRY_DELAY} seconds...")
            await asyncio.sleep(RETRY_DELAY)
    
    if retries == MAX_RETRIES:
        logging.error("Max retries reached. Could not connect to the database.")
        raise Exception("Database connection failed after max retries.")

async def close_db(app):
    await app['db'].close()

async def init_schema(app):
    async with app['db'].acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id SERIAL PRIMARY KEY,
                measurement_type VARCHAR(100) NOT NULL,
                time INT NOT NULL,
                value FLOAT NOT NULL
            );
        ''')
        logging.info("Database schema initialized.")

async def save_measurements(app, measurement_type, values):
    async with app['db'].acquire() as conn:
        async with conn.transaction():
            for record in values:
                await conn.execute(
                    "INSERT INTO measurements (measurement_type, time, value) VALUES ($1, $2, $3)",
                    measurement_type, record['time'], record['value']
                )

async def get_measurements(app, measurement_types, from_time, to_time):
    async with app['db'].acquire() as conn:
        results = {}
        for measurement_type in measurement_types:
            records = await conn.fetch(
                "SELECT time, value FROM measurements WHERE measurement_type=$1 AND time BETWEEN $2 AND $3",
                measurement_type, from_time, to_time
            )
            results[measurement_type] = [{'time': r['time'], 'value': r['value']} for r in records]
        return results
