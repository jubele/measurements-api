import os
import pytest
from freezegun import freeze_time

from db import init_db

@freeze_time("Jan 14th, 2020", auto_tick_seconds=5)
@pytest.mark.asyncio
async def test_init_db_raises_exception_with_invalid_credentials():
    os.environ['PG_USER'] = 'invalid_user'
    os.environ['PG_PWD'] = 'invalid_password'
    app = {}
    with pytest.raises(Exception) as exc_info:
        await init_db(app)
    assert str(exc_info.value) == "Database connection failed after max retries."