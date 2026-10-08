import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    ct_btn = page.locator("button:has-text('Confirm time')").first
    print("Confirm time button found:", ct_btn.count() > 0, "visible:", ct_btn.is_visible())
    if ct_btn.is_visible():
        print("Clicking Confirm time...")
        ct_btn.click()
        page.wait_for_timeout(3000)

    # Screenshot after Confirm time
    page.screenshot(path="handshake/scratch/after_confirm_time_final.png")
    print("Saved screenshot to handshake/scratch/after_confirm_time_final.png")
    print("Current URL:", page.url)
    print("Page Title:", page.title())
    body_txt = page.locator("body").inner_text()[:600].replace('\n', ' ')
    print("Body text snippet:\n", body_txt)
