import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    sub = page.locator("button:has-text('Submit task')").first
    print("HTML:", sub.evaluate("el => el.outerHTML"))
    print("Disabled:", sub.evaluate("el => el.disabled"))
    print("Aria-disabled:", sub.evaluate("el => el.getAttribute('aria-disabled')"))
