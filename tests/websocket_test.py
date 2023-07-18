import pytest
import websockets
import json
import aiohttp


async def post_order(url, quantity):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={
            'stock_symbol': 'EURUSD',
            'quantity': quantity
        }) as resp:
            assert resp.status == 201
            data = await resp.json()
            return data['id']


class TestWebSocket:

    @pytest.mark.asyncio
    async def test_ws_status_change(self, base_ws, base_url):
        async with websockets.connect(f'{base_ws}/ws') as ws_connection:
            assert ws_connection.open

            order_id = await post_order(f'{base_url}/orders', 100.0)

            subscribe_message = {
                "action": "subscribe",
                "order_id": order_id,
            }

            await ws_connection.send(json.dumps(subscribe_message))

            update = await ws_connection.recv()
            message = json.loads(update)
            assert message == {"order_id": order_id, "new_status": "EXECUTED"}
