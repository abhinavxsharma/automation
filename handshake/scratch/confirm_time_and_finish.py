import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    print("Checking for Confirm time button...")
    confirm_btn = page.locator("button:has-text('Confirm time')").first
    if confirm_btn.is_visible():
        print("Clicking Confirm time button...")
        confirm_btn.click()
        page.wait_for_timeout(4000)

    page.screenshot(path="scratch/after_confirm_time.png")
    print("Saved screenshot to scratch/after_confirm_time.png")
    print("Final URL:", page.url)
    print("Final Title:", page.title())
