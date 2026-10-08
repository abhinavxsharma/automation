import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    print("URL:", page.url)
    print("Title:", page.title())
    body_text = page.locator("body").inner_text()
    print("Body length:", len(body_text))
    print("Body preview:\n", body_text[:600])
    page.screenshot(path="handshake/scratch/current_page_state.png")
