import pytest


@pytest.fixture
def new_order_data(order_schema):
    data = {
        'stock_symbol': 'EURUSD',
        'quantity': 1000.0
    }
    order_schema.validate_input(data)
    return data


class TestOrders:

    def test_get_all_orders(self, api_client, order_schema):
        response = api_client.get_orders()
        assert response.status_code == 200
        orders = response.json()
        order_schema.validate_list_output(orders)

    def test_post_order(self, api_client, new_order_data, order_schema):
        response = api_client.post_order(new_order_data)
        assert response.status_code == 201
        created_order = response.json()
        order_schema.validate_output(created_order)
        assert created_order['stock_symbol'] == new_order_data['stock_symbol']
        assert created_order['quantity'] == new_order_data['quantity']

    def test_get_specific_order(self, api_client, new_order_data, order_schema):
        response = api_client.post_order(new_order_data)
        order_id = response.json()['id']

        get_response = api_client.get_order(order_id)
        assert get_response.status_code == 200
        order = get_response.json()
        order_schema.validate_output(order)

        assert order['id'] == order_id
        assert order['stock_symbol'] == new_order_data['stock_symbol']
        assert order['quantity'] == new_order_data['quantity']

    def test_delete_order(self, api_client, new_order_data, order_schema, error_schema):
        response = api_client.post_order(new_order_data)
        order_id = response.json()['id']

        delete_response = api_client.delete_order(order_id)
        assert delete_response.status_code == 204

        get_response = api_client.get_order(order_id)
        assert get_response.status_code == 404
        error = get_response.json()
        error_schema.validate_error(error)

    def test_get_non_existing_order(self, api_client, error_schema, not_used_uuid):
        response = api_client.get_order(not_used_uuid)
        assert response.status_code == 404
        error = response.json()
        error_schema.validate_error(error)

    def test_delete_non_existing_order(self, api_client, error_schema, not_used_uuid):
        response = api_client.delete_order(not_used_uuid)
        assert response.status_code == 404
        error = response.json()
        error_schema.validate_error(error)

    def test_place_order_with_invalid_input(self, api_client, error_schema):
        invalid_input = {'quantity': 1000.0}
        response = api_client.post_order(invalid_input)
        assert response.status_code == 400
        error = response.json()
        error_schema.validate_error(error)

    def test_place_order_with_wrong_type_input(self, api_client, error_schema):
        wrong_type_input = {'stock_symbol': 'EURUSD', 'quantity': 'a lot'}
        response = api_client.post_order(wrong_type_input)
        assert response.status_code == 400
        error = response.json()
        error_schema.validate_error(error)

    def test_place_order_with_additional_fields(self, api_client, error_schema):
        additional_fields_input = {'stock_symbol': 'EURUSD', 'quantity': 1000.0, 'additional': 'field'}
        response = api_client.post_order(additional_fields_input)
        assert response.status_code == 400
        error = response.json()
        error_schema.validate_error(error)

    def test_place_order_with_negative_quantity(self, api_client, error_schema):
        negative_quantity_input = {'stoks': 'EURUSD', 'quantity': -1000.0}
        response = api_client.post_order(negative_quantity_input)
        assert response.status_code == 400
        error = response.json()
        error_schema.validate_error(error)

    def test_place_order_with_no_quantity(self, api_client, error_schema):
        no_quantity_input = {'stoks': 'EURUSD'}
        response = api_client.post_order(no_quantity_input)
        assert response.status_code == 400
        error = response.json()
        error_schema.validate_error(error)

    def test_place_order_with_non_string_stocks(self, api_client, error_schema):
        non_string_stocks_input = {'stoks': 1000, 'quantity': 1000.0}
        response = api_client.post_order(non_string_stocks_input)
        assert response.status_code == 400
        error = response.json()
        error_schema.validate_error(error)

    def test_delete_order_twice(self, api_client, new_order_data, order_schema, error_schema):
        response = api_client.post_order(new_order_data)
        order_id = response.json()['id']

        delete_response1 = api_client.delete_order(order_id)
        assert delete_response1.status_code == 204

        delete_response2 = api_client.delete_order(order_id)
        assert delete_response2.status_code == 404
        error = delete_response2.json()
        error_schema.validate_error(error)
