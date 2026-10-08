import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    save_btn = page.locator("button:has-text('Save')").first
    print("Save button visible:", save_btn.is_visible())
    save_btn.click()
    page.wait_for_timeout(2000)

    page.screenshot(path="handshake/scratch/after_top_save_clicked.png")
    print("Screenshot saved to handshake/scratch/after_top_save_clicked.png")
