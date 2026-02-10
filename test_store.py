from jsonschema import validate
import pytest
import schemas
import api_helpers
from hamcrest import assert_that, contains_string, is_


@pytest.fixture
def create_order():
    """
    Fixture to create a unique test order for each test run.
    Dynamically finds an available pet and creates an order with it.
    Returns the order_id for use in tests.
    """
    # Get all pets and find one that is available
    response = api_helpers.get_api_data("/pets")
    pets = response.json()
    
    # Find the first available pet
    available_pet = None
    for pet in pets:
        if pet['status'] == 'available':
            available_pet = pet
            break
    
    assert available_pet is not None, "No available pets found to create an order"
    
    # Create an order with the available pet
    order_data = {"pet_id": available_pet['id']}
    response = api_helpers.post_api_data("/store/order", order_data)
    assert response.status_code == 201, f"Failed to create order: {response.status_code} - {response.text}"
    
    order = response.json()
    return order['id']


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
