import pytest
from playwright.sync_api import APIRequestContext

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_product_detail(playwright):
    # Initialize API context and first GET API request.
    api_context = playwright.request.new_context(base_url=BASE_URL)
    response = api_context.get("/posts/1")
    
    assert response.ok, f"API requet failed with status {response.status}"
    assert response.status == 200

    assert response["id"] == 1
    assert "title" in response
    assert "body" in response
    
    api_context.dispose()