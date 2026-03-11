import pytest
from playwright.sync_api import sync_playwright
from _pytest.python import Metafunc

@pytest.fixture(scope='function')
def new_page(request):
    """
    Creates a new browser page instance for each test.
    Function suppots cross-browser testing via parametrization.
    """
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=True, slow_mo=1500, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1920, 'height': 1000}, user_agent="Mozilla/5.0 (Windows NT 10.0; AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def pytest_generate_tests(metafunc: Metafunc):
    if "new_page" in metafunc.fixturenames:
        metafunc.parametrize("new_page", ["chromium"], indirect=True) #One browser for faster testing