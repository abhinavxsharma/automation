import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    btns = page.locator("button").all()
    for b in btns:
        if b.is_visible():
            txt = b.inner_text().strip()
            aria = b.get_attribute("aria-label") or ""
            print(f"Visible button: txt='{txt}' aria='{aria}'")
