import os
import pytest
from playwright.sync_api import sync_playwright
from _pytest.python import Metafunc
from datetime import datetime

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        page = item.funcargs.get("new_page") or item.funcargs.get("page")

        if page:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            screenshot_dir = os.path.join(base_dir, "screenshots")
            os.makedirs(screenshot_dir, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            file_name = f"FAILED_{item.name}_{timestamp}.png"
            path = os.path.join(screenshot_dir, file_name)

            page.screenshot(path=path, full_page=True)
            print(f"\nFailure screenshot saved: {path}")

@pytest.fixture(scope='function')
def new_page(request):
    """
    Creates a new browser page instance for each test.
    Function suppots cross-browser testing via parametrization.
    """
    browser_name = request.param
    with sync_playwright() as p:
        browser_type = getattr(p, browser_name)
        browser = browser_type.launch(headless=False, slow_mo=1500, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(viewport={'width': 1920, 'height': 1000}, user_agent="Mozilla/5.0 (Windows NT 10.0; AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
        page = context.new_page()
        yield page
        context.close()
        browser.close()

def pytest_generate_tests(metafunc: Metafunc):
    if "new_page" in metafunc.fixturenames:
        metafunc.parametrize("new_page", ["chromium"], indirect=True) #One browser for faster testing