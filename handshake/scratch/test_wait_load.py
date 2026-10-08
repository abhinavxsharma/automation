import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    print("Title:", page.title())
    print("Save button count:", page.locator("button:has-text('Save')").count())
    body_text = page.evaluate("() => document.body.innerText")
    print("Body text length:", len(body_text))
    print("Sample body text:\n", body_text[:300])
