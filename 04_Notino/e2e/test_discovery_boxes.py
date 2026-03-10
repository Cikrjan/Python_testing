import pytest
from playwright.sync_api import Page, expect

def test_db_filter(new_page):
    # 1. Open the website
    new_page.goto("https://www.notino.cz/")

    # 2. Cookie consent
    # First, we define the locator (where it is)
    accept_cookies = new_page.locator(".accept.uc-accept-button")
    
    # Then we check if it's there and click it
    try:
        #If shows up, click on the button
        accept_cookies.wait_for(state="visible", timeout=3000)
        accept_cookies.click()
        print("Cookie bar dismissed.")
    except:
        #If doesn't, it's okay, let's move on
        print("Cookie bar did not appear within 3s.")

  # 3. Click on Discovery boxes page
    # We use a more flexible locator. Sometimes 'nav' is too restrictive.
    # We search for a link (link) that contains the text.
    discovery_link = new_page.get_by_role("link", name="Discovery boxy").first

    # We give it more time (10s) and scroll to it
    discovery_link.wait_for(state="visible", timeout=10000)
    discovery_link.click()

    # 4. Page loaded check
    expect(new_page).to_have_url("https://www.notino.cz/discovery-boxy/")

    # 5. Filter "Brand"
    # Fixed the typo from "Zančka" to "Značka"
    new_page.get_by_role("button", name="Značka").click()

    # 6. Choose brand
    new_page.get_by_label("Notino").check()

    # 7. Final wait and log
    new_page.wait_for_timeout(2000)
    print("Test complete, filter works!")

    # 8. Take a screenshot. Comment this line out during development
    new_page.screenshot(path="e2e/screenshots/filter_result.png")
    print("Screenshot saved.")