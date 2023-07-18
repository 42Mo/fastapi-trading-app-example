import pytest
import requests
import json
from jsonschema import validate
from tests.schemas import error_schema, order_output_schema, orders_output_schema
import uuid


@pytest.fixture
def order_input():
    return {
        'stock_symbol': 'EURUSD',
        'quantity': 1000.0
    }


class TestOrders:

    def test_get_all_orders(self, base_url):
        response = requests.get(f'{base_url}/orders')
        assert response.status_code == 200
        orders = response.json()
        validate(instance=orders, schema=orders_output_schema)

    def test_post_order(self, base_url, order_input):
        response = requests.post(f'{base_url}/orders', data=json.dumps(order_input), headers={'Content-Type': 'application/json'})
        assert response.status_code == 201
        order = response.json()
        validate(instance=order, schema=order_output_schema)
        assert order['stock_symbol'] == order_input['stock_symbol']
        assert order['quantity'] == order_input['quantity']

    def test_get_specific_order(self, base_url, order_input):
        post_response = requests.post(f'{base_url}/orders', data=json.dumps(order_input), headers={'Content-Type': 'application/json'})
        order_id = post_response.json()['id']
        get_response = requests.get(f'{base_url}/orders/{order_id}')
        assert get_response.status_code == 200
        order = get_response.json()
        validate(instance=order, schema=order_output_schema)
        assert order['id'] == order_id
        assert order['stock_symbol'] == order_input['stock_symbol']
        assert order['quantity'] == order_input['quantity']

    def test_delete_order(self, base_url, order_input):
        post_response = requests.post(f'{base_url}/orders', data=json.dumps(order_input), headers={'Content-Type': 'application/json'})
        order_id = post_response.json()['id']
        delete_response = requests.delete(f'{base_url}/orders/{order_id}')
        assert delete_response.status_code == 204
        get_response = requests.get(f'{base_url}/orders/{order_id}')
        assert get_response.status_code == 404
        error = get_response.json()
        validate(instance=error, schema=error_schema)

    def test_get_non_existing_order(self, base_url):
        random_id = str(uuid.uuid4())
        response = requests.get(f'{base_url}/orders/{random_id}')
        assert response.status_code == 404
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test delete non-existing order
    def test_delete_non_existing_order(self, base_url):
        random_id = str(uuid.uuid4())
        response = requests.delete(f'{base_url}/orders/{random_id}')
        assert response.status_code == 404
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with invalid input (missing fields)
    def test_place_order_with_invalid_input(self, base_url):
        invalid_input = {'quantity': 1000.0}  # 'stoks' field is missing
        response = requests.post(f'{base_url}/orders', data=json.dumps(invalid_input),
                                 headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with invalid input (wrong type)
    def test_place_order_with_wrong_type_input(self, base_url):
        wrong_type_input = {'stoks': 'EURUSD', 'quantity': 'a lot'}  # 'quantity' should be a number
        response = requests.post(f'{base_url}/orders', data=json.dumps(wrong_type_input),
                                 headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with invalid input (additional fields)
    def test_place_order_with_additional_fields(self, base_url):
        additional_fields_input = {'stoks': 'EURUSD', 'quantity': 1000.0,
                                   'additional': 'field'}  # Additional fields should not be accepted
        response = requests.post(f'{base_url}/orders', data=json.dumps(additional_fields_input),
                                 headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with invalid quantity (negative value)
    def test_place_order_with_negative_quantity(self, base_url):
        negative_quantity_input = {'stoks': 'EURUSD', 'quantity': -1000.0}
        response = requests.post(f'{base_url}/orders', data=json.dumps(negative_quantity_input), headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with no quantity
    def test_place_order_with_no_quantity(self, base_url):
        no_quantity_input = {'stoks': 'EURUSD'}
        response = requests.post(f'{base_url}/orders', data=json.dumps(no_quantity_input), headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with no stocks
    def test_place_order_with_no_stocks(self, base_url):
        no_stocks_input = {'quantity': 1000.0}
        response = requests.post(f'{base_url}/orders', data=json.dumps(no_stocks_input), headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test place order with non-string stocks
    def test_place_order_with_non_string_stocks(self, base_url):
        non_string_stocks_input = {'stoks': 1000, 'quantity': 1000.0}
        response = requests.post(f'{base_url}/orders', data=json.dumps(non_string_stocks_input), headers={'Content-Type': 'application/json'})
        assert response.status_code == 400
        error = response.json()
        validate(instance=error, schema=error_schema)

    # Test delete order twice
    def test_delete_order_twice(self, order_input, base_url):
        post_response = requests.post(f'{base_url}/orders', data=json.dumps(order_input), headers={'Content-Type': 'application/json'})
        order_id = post_response.json()['id']
        delete_response1 = requests.delete(f'{base_url}/orders/{order_id}')
        assert delete_response1.status_code == 204
        delete_response2 = requests.delete(f'{base_url}/orders/{order_id}')
        assert delete_response2.status_code == 404
        error = delete_response2.json()
        validate(instance=error, schema=error_schema)