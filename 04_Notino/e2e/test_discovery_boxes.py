import os
import pytest
from playwright.sync_api import Page, expect

def test_db_filter(new_page: Page):
    #Create folder for screenshots
    os.makedirs("04_Notino/e2e/screenshots", exist_ok=True)
    # 1. Open the website
    new_page.goto("https://www.notino.cz/")

    # 2. Cookie consent
    # First, we define the locator (find those cookies!)
    accept_cookies = new_page.locator(".accept.uc-accept-button")
    
    # Then we check if it's there and click it
    try:
        #If it shows up, click on the button
        accept_cookies.wait_for(state="visible", timeout=3000)
        accept_cookies.click()
        print("Cookie bar dismissed.")
    except:
        #If doesn't, it's okay, let's move on
        print("Cookie bar did not appear within 3s.")

  # 3. Discovery boxes are hidden under 'Inspirace' hover menu, so I need to locate it first.
    new_page.get_by_text("Inspirace").first.hover()
    new_page.wait_for_timeout(2000)
    #Then I can locate 'Discovery boxy'
    DB_link = new_page.get_by_role("link", name="Discovery boxy").first

    # Give it more time (3s), after that click on it
    DB_link.wait_for(state="visible", timeout=10000)
    DB_link.click()

    # 4. Page loaded check
    expect(new_page).to_have_url("https://www.notino.cz/beauty/?f=1-1-44128-77223")
    print("Discovery boxes url load check")

    # 5. Filter for 'Parfémy' and pick only the best (5-star reviews) under 'Hodnocení' section.
    perfumes = new_page.get_by_role("link", name="Parfémy").first
    perfumes.click(force=True, timeout=10000)

    #6 Are we on the same page? (Pun intended) Great, print success message.
    expect(new_page).to_have_url("https://www.notino.cz/beauty/?f=1-1-44128-55544-77223")
    print("Test complete, filter works!")

    #6.1 Are we not? Never mind, save the screenshot for work on improvement.
    new_page.screenshot(path="04_Notino/e2e/screenshots/final_state.png", full_page=True)
    print("Screenshot has been saved.")