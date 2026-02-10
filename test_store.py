from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


@pytest.fixture
def create_order():
    """
    Fixture to create a unique test order for each test run.
    Returns the order_id for use in tests.
    """
    # Try to create an order with an available pet
    # Pets 0 and 2 start as available, but may be used by previous tests
    for pet_id in [0, 2]:
        order_data = {"pet_id": pet_id}
        response = api_helpers.post_api_data("/store/order", order_data)
        if response.status_code == 201:
            order = response.json()
            return order['id']
    # If both fail, raise an error with details
    raise Exception("Could not create order: no available pets found")


'''
TODO: Finish this test by...
1) Creating a function to test the PATCH request /store/order/{order_id}
2) *Optional* Consider using @pytest.fixture to create unique test data for each run
2) *Optional* Consider creating an 'Order' model in schemas.py and validating it in the test
3) Validate the response codes and values
4) Validate the response message "Order and pet status updated successfully"
'''
@pytest.mark.parametrize("new_status", ["sold", "available", "pending"])
def test_patch_order_by_id(create_order, new_status):
    order_id = create_order
    test_endpoint = f"/store/order/{order_id}"
    update_data = {"status": new_status}
    
    response = api_helpers.patch_api_data(test_endpoint, update_data)
    
    # Validate the response code
    assert response.status_code == 200
    
    # Get the response data
    response_data = response.json()
    
    # Validate the response message
    assert_that(response_data['message'], contains_string("Order and pet status updated successfully"))
