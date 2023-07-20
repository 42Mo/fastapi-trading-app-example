import pytest
import os
import uuid
from utils.api_client import ApiClient
from tests.schemas.order import OrderSchema
from tests.schemas.error import ErrorSchema


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


@pytest.fixture(scope="session")
def api_client(base_url):
    return ApiClient(base_url)


@pytest.fixture
def order_schema():
    return OrderSchema


@pytest.fixture
def error_schema():
    return ErrorSchema


@pytest.fixture(scope='session')
def not_used_uuid():
    return str(uuid.uuid4())
