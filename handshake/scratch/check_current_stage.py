import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    print("Current URL:", page.url)
    print("Page Title:", page.title())
    
    # Check top nav text
    body_txt = page.locator("body").inner_text()
    print("Body preview (first 1000 chars):\n", body_txt[:1000])

    page.screenshot(path="handshake/scratch/current_stage_check.png")
    print("Screenshot saved to handshake/scratch/current_stage_check.png")
