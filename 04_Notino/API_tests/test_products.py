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

def test_create_new_product(playwright):
    # Initialize API context for POST request
    api_context = playwright.request.new_context(base_url=BASE_URL)

    # Payload which simulating adding a new perfume into listing
    new_product_payload = {
        "userId": 1996,
        "language": "CZ",
        "title": "Armani Acqua di Giò",
        "body": "Toaletní voda pro muže 100 ml - ikonická svěží vůně"
    }

    # Send POST request with payload 
    response = api_context.post("/posts", data=new_product_payload)

    # Verification
    assert response.status == 201

    # Validation, that server processed and return corrext data
    response_data = response.json()
    assert response_data["title"] == "Armani Acqua di Giò"
    assert response_data["userId"] == 1996
    assert response_data["language"] == "CZ"
    
    api_context.dispose()