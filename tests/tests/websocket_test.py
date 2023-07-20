import pytest
import websockets
import json


@pytest.fixture
def new_order_data(order_schema):
    data = {
        'stock_symbol': 'EURUSD',
        'quantity': 1000.0
    }
    order_schema.validate_input(data)
    return data


class TestWebSocket:

    @pytest.mark.asyncio
    async def test_ws_status_change(self, base_ws, api_client, new_order_data):
        async with websockets.connect(f'{base_ws}/ws') as ws_connection:
            assert ws_connection.open

            response = await api_client.post_order_async(new_order_data)
            order_id = response['id']

            subscribe_message = {
                "action": "subscribe",
                "order_id": order_id,
            }

            await ws_connection.send(json.dumps(subscribe_message))

            update = await ws_connection.recv()
            message = json.loads(update)
            assert message == {"order_id": order_id, "new_status": "EXECUTED"}
