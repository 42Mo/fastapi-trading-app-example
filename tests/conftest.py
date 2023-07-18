import pytest
import os


@pytest.fixture(scope='session')
def base_url():
    host = os.getenv('BASE_HOST', 'localhost')
    port = os.getenv('BASE_PORT', '8080')
    return f"http://{host}:{port}"


@pytest.fixture(scope='session')
def base_ws():
    host = os.getenv('BASE_HOST', 'localhost')
    port = os.getenv('BASE_PORT', '8080')
    return f"ws://{host}:{port}"