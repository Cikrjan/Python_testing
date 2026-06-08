import pytest

BASE_URL = "https://jsonplaceholder.typicode.com"

def test_get_product_detail(playwright):
    # Initialize API context and first GET API request.
    api_context = playwright.request.new_context(base_url=BASE_URL)
    response = api_context.get("/posts/1")
    
    # Print response JSON to verify the data structure
    print(response.json())
    
    api_context.dispose()