import aiohttp
import requests


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def post_order(self, order):
        return self.session.post(
            f"{self.base_url}/orders",
            json=order,
            headers={'Content-Type': 'application/json'}
        )

    async def post_order_async(self, order):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/orders",
                json=order,
                headers={'Content-Type': 'application/json'}
            ) as response:
                assert response.status == 201
                data = await response.json()
                return data

    def get_orders(self):
        return self.session.get(f"{self.base_url}/orders")

    def get_order(self, order_id):
        return self.session.get(f"{self.base_url}/orders/{order_id}")

    def delete_order(self, order_id):
        return self.session.delete(f"{self.base_url}/orders/{order_id}")
