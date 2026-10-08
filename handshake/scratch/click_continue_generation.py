from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Click Continue button on the card: "Click continue to generate a new response using this prompt."
    cont_btn = page.locator("button:has-text('Continue')").first
    if cont_btn.is_visible(timeout=3000):
        print("Clicking Continue button to start response generation...")
        cont_btn.click(force=True)
        page.wait_for_timeout(3000)
    else:
        print("Continue button not visible!")

    page.screenshot(path="scratch/after_click_continue_generation.png")
    print("Saved scratch/after_click_continue_generation.png")
