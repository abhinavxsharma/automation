import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    cancel_btn = page.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible():
        cancel_btn.click()
        print("Clicked Cancel on Prompt editor.")
        page.wait_for_timeout(1000)
    page.screenshot(path="handshake/scratch/after_prompt_cancel.png")
