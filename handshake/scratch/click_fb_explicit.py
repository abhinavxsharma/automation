import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    btn = page.locator("button[aria-label='Feedback']").first
    print("Feedback button count:", page.locator("button[aria-label='Feedback']").count())
    print("Feedback button is_visible:", btn.is_visible())
    print("Bounding box:", btn.bounding_box())
    if btn.is_visible():
        btn.click()
        page.wait_for_timeout(1500)
    page.screenshot(path="scratch/after_fb_explicit_click.png")
