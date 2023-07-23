import pytest
import allure


@pytest.fixture
def new_order_data(order_schema):
    data = {
        'stock_symbol': 'EURUSD',
        'quantity': 1000.0
    }
    order_schema.validate_input(data)
    return data


@pytest.mark.orders
@allure.feature('Orders')
@allure.story('Orders API')
class TestOrders:

    @allure.title('Get all orders')
    def test_get_all_orders(self, api_client, order_schema):
        response = api_client.get_orders()

        with allure.step("Validate response code"):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code} instead."

        orders = response.json()
        order_schema.validate_list_output(orders)

    @allure.title('Create an order')
    def test_post_order(self, api_client, new_order_data, order_schema):
        response = api_client.post_order(new_order_data)

        with allure.step("Validate response code"):
            assert response.status_code == 201, f"Expected status code 201, but got {response.status_code} instead."

        created_order = response.json()
        order_schema.validate_output(created_order)

        with allure.step("Validate created order"):
            assert created_order['stock_symbol'] == new_order_data['stock_symbol']
            assert created_order['quantity'] == new_order_data['quantity']

    @allure.title('Get an order by id')
    def test_get_specific_order(self, api_client, new_order_data, order_schema):
        response = api_client.post_order(new_order_data)
        order_id = response.json()['id']

        get_response = api_client.get_order(order_id)

        with allure.step("Validate response code"):
            assert get_response.status_code == 200, f"Expected status code 200, but got {response.status_code} instead."

        order = get_response.json()
        order_schema.validate_output(order)

        with allure.step("Validate fetched order"):
            assert order['id'] == order_id
            assert order['stock_symbol'] == new_order_data['stock_symbol']
            assert order['quantity'] == new_order_data['quantity']

    @allure.title('Delete an order by id')
    def test_delete_order(self, api_client, new_order_data, error_schema):
        response = api_client.post_order(new_order_data)
        order_id = response.json()['id']

        delete_response = api_client.delete_order(order_id)

        with allure.step("Validate response code"):
            assert delete_response.status_code == 204, f"Expected status code 204, but got {response.status_code} instead."

        get_response = api_client.get_order(order_id)

        with allure.step("Validate response code"):
            assert get_response.status_code == 404, f"Expected status code 404, but got {response.status_code} instead."

        error = get_response.json()
        error_schema.validate_error(error)

    @allure.title('Get non existing order')
    def test_get_non_existing_order(self, api_client, error_schema, not_used_uuid):
        response = api_client.get_order(not_used_uuid)

        with allure.step("Validate response code"):
            assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Delete non existing order')
    def test_delete_non_existing_order(self, api_client, error_schema, not_used_uuid):
        response = api_client.delete_order(not_used_uuid)

        with allure.step("Validate response code"):
            assert response.status_code == 404, f"Expected status code 404, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Create an order with "quantity" missing')
    def test_place_order_with_invalid_input(self, api_client, error_schema):
        invalid_input = {'quantity': 1000.0}
        response = api_client.post_order(invalid_input)

        with allure.step("Validate response code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Create an order with "quantity" of wrong type')
    def test_place_order_with_wrong_type_input(self, api_client, error_schema):
        wrong_type_input = {'stock_symbol': 'EURUSD', 'quantity': 'a lot'}
        response = api_client.post_order(wrong_type_input)

        with allure.step("Validate response code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Create an order with additional field')
    def test_place_order_with_additional_fields(self, api_client, error_schema):
        additional_fields_input = {'stock_symbol': 'EURUSD', 'quantity': 1000.0, 'additional': 'field'}
        response = api_client.post_order(additional_fields_input)

        with allure.step("Validate response code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Create an order with negative quantity')
    def test_place_order_with_negative_quantity(self, api_client, error_schema):
        negative_quantity_input = {'stock_symbol': 'EURUSD', 'quantity': -1000.0}
        response = api_client.post_order(negative_quantity_input)

        with allure.step("Validate response code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Create an order with "stock_symbol" missing')
    def test_place_order_with_no_stock_symbol(self, api_client, error_schema):
        no_quantity_input = {'quantity': 1000.0}
        response = api_client.post_order(no_quantity_input)

        with allure.step("Validate response code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Create an order with "stock_symbol" of wrong type')
    def test_place_order_with_non_string_stocks(self, api_client, error_schema):
        non_string_stocks_input = {'stock_symbol': 1000, 'quantity': 1000.0}
        response = api_client.post_order(non_string_stocks_input)

        with allure.step("Validate response code"):
            assert response.status_code == 400, f"Expected status code 400, but got {response.status_code} instead."

        error = response.json()
        error_schema.validate_error(error)

    @allure.title('Delete an order twice')
    def test_delete_order_twice(self, api_client, new_order_data, error_schema):
        response = api_client.post_order(new_order_data)
        order_id = response.json()['id']

        delete_response1 = api_client.delete_order(order_id)

        with allure.step("Validate first delete response code"):
            assert delete_response1.status_code == 204,\
                f"Expected status code 204, but got {response.status_code} instead."

        delete_response2 = api_client.delete_order(order_id)

        with allure.step("Validate second delete response code"):
            assert delete_response2.status_code == 404,\
                f"Expected status code 404, but got {response.status_code} instead."

        error = delete_response2.json()
        error_schema.validate_error(error)
