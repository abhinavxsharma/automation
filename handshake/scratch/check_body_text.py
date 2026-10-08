from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    text = page.evaluate("() => document.body ? document.body.innerText : 'NO BODY'")
    print("Length of body text:", len(text))
    print("Body text snippet:\n", text[:800])
