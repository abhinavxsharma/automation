from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        st_btn.click()
        page.wait_for_timeout(1000)
        print("Dismissed Start timer modal.")

    page.screenshot(path="scratch/after_modal_dismissed.png")
    print("Saved scratch/after_modal_dismissed.png")
