import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # Dismiss timer if visible
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        btn.click()
        page.wait_for_timeout(500)

    # Let's inspect the top-bar Save button
    top_save = page.locator("button:has-text('Save')").first
    print("Top save visible:", top_save.is_visible())
    print("Top save disabled:", top_save.is_disabled())

    # Open Step 7
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    edit_btns[7].scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    edit_btns[7].click()
    page.wait_for_timeout(1000)

    # Check top save again
    print("Top save disabled after opening editor:", top_save.is_disabled())

    # Cancel editor to be safe
    cancel_btn = page.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible():
        cancel_btn.click()
        page.wait_for_timeout(1000)
        print("Cancelled editor safely.")
