import pytest
from playwright.sync_api import Page, expect

def test_db_filter(new_page: Page):
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
    new_page.locator("[data-cypress='mainMenu-Inspirace']").nth(1).hover()
    
    #Then I can locate "Discovery boxy"
    DB_link = new_page.get_by_role("link", name="Discovery boxy").first

    # Give it time, after that click on it
    DB_link.wait_for(state="visible", timeout=10000)
    DB_link.click()

    # 4. Are we on the same page? (Pun intended) Great, print success message.
    expect(new_page).to_have_url("https://www.notino.cz/beauty/?f=1-1-44128-77223")
    print("Discovery boxes url load check")

    # 5. Filter for 'Parfémy'.
    perfumes = new_page.get_by_test_id("navigation-tree").get_by_role("link", name="Parfémy").first
    perfumes.click(force=True)

    expect(new_page).to_have_url("https://www.notino.cz/beauty/?f=1-1-44128-55544-77223")
    print("Perfumes selected, test complete.")

    # 6 And of course we want only the best. Filter 5-star review.
    new_page.locator("label").filter(has_text="5,019").click()

    expect(new_page).to_have_url("https://www.notino.cz/beauty/?f=1-1-44128-55544-77223-200005")
    print("Selected by 5-star review page.")

    five_star_review_products = new_page.get_by_test_id("product-container").first
    expect(five_star_review_products).to_contain_text("5,0")
    print("Verification that we have 5-star review products displayed.")