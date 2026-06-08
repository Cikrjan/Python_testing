import pytest
from playwright.sync_api import APIRequestContext

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_product_detail(playwright):
    # Initialize API context and send GET request.
    api_context = playwright.request.new_context(base_url=BASE_URL)
    response = api_context.get("/posts/1")
    
    # Add assertion and warning line in case of invalid response.
    assert response.ok, f"API request failed with status {response.status}"
    assert response.status == 200

    # Parsing response to JSON
    response_data = response.json()

    # Data validation
    assert response_data["id"] == 1
    assert "title" in response_data
    assert "body" in response_data

    api_context.dispose()