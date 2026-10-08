import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        print("Clicking Start timer to dismiss modal...")
        st_btn.click(force=True)
        page.wait_for_timeout(1500)

    # Check for Got it toast
    got_it = page.locator("button:has-text('Got it')").first
    if got_it.is_visible(timeout=1000):
        got_it.click(force=True)
        page.wait_for_timeout(500)

    # Check for Continue button
    cont_btn = page.locator("button:has-text('Continue')").first
    if cont_btn.is_visible(timeout=2000):
        print("Found Continue button! Clicking it...")
        cont_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        cont_btn.click(force=True)
        page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_dismiss_and_continue.png")
    print("Saved scratch/after_dismiss_and_continue.png")
