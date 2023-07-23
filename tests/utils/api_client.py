import aiohttp
import allure
import json
from requests import Session
from datetime import datetime


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = Session()

    @allure.step('Making GET request to "{url}"')
    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

    @allure.step('Making POST request to "{url}"')
    def post(self, url, **kwargs):
        return self.session.post(url, **kwargs)

    @allure.step('Making DELETE request to "{url}"')
    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)

    @staticmethod
    def parse_response(response):
        try:
            response_body = json.loads(response.text)
        except json.JSONDecodeError:
            response_body = response.text

        return {
            'url': response.url,
            'status_code': response.status_code,
            'response_headers': dict(response.headers),
            'response_body': response_body,
            'timestamp': datetime.now().isoformat(),
            'duration': response.elapsed.total_seconds()
        }

    @allure.step('Creating order with data "{order}"')
    def post_order(self, order, headers=None):
        headers = headers or {'Content-Type': 'application/json'}
        response = self.post(
            f"{self.base_url}/orders",
            json=order,
            headers=headers
        )
        allure.attach(
            json.dumps(ApiClient.parse_response(response), indent=2),
            name="Response info",
            attachment_type=allure.attachment_type.JSON
        )
        return response

    @allure.step('[Async] Creating order with data "{order}"')
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

    @allure.step('Fetching list of orders')
    def get_orders(self):
        response = self.get(f"{self.base_url}/orders")
        allure.attach(
            json.dumps(ApiClient.parse_response(response), indent=2),
            name="Response info",
            attachment_type=allure.attachment_type.JSON
        )
        return response

    @allure.step('Fetching order with id "{order_id}"')
    def get_order(self, order_id):
        response = self.get(f"{self.base_url}/orders/{order_id}")
        allure.attach(
            json.dumps(ApiClient.parse_response(response), indent=2),
            name="Response info",
            attachment_type=allure.attachment_type.JSON
        )
        return response

    @allure.step('Deleting order with id "{order_id}"')
    def delete_order(self, order_id):
        response = self.delete(f"{self.base_url}/orders/{order_id}")
        allure.attach(
            json.dumps(ApiClient.parse_response(response), indent=2),
            name="Response info",
            attachment_type=allure.attachment_type.JSON
        )
        return response
