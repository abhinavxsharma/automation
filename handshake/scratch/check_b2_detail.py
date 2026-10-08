import sys

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)

    # Check Continue button status
    cont_btn = page.locator("button:has-text('Continue')").last
    if cont_btn.is_visible():
        is_disabled = cont_btn.is_disabled()
        text = cont_btn.inner_text()
        print(f"Continue button: disabled={is_disabled} text='{text}'")

    # Check Block 2 section
    b2_el = page.locator("div:has-text('Block 2 Responses:')").last
    if b2_el.is_visible():
        print("Block 2 text preview:\n", b2_el.inner_text()[:400])

    page.screenshot(path="scratch/check_b2_live.png")
    print("Screenshot saved to scratch/check_b2_live.png")
