import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(20):
        if "Continue" in page.evaluate("() => document.body ? document.body.innerText : ''"):
            break
        time.sleep(0.5)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(500)

    cont_btn = page.locator("button:has-text('Continue')").last
    if cont_btn.is_visible():
        print("Clicking Continue button...")
        cont_btn.click(force=True)
        page.wait_for_timeout(3000)

    page.screenshot(path="scratch/after_b2_continue_click.png")
    print("Saved scratch/after_b2_continue_click.png")

    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    for ln in text.splitlines():
        if any(w in ln for w in ["Block", "Generating", "Final Answer", "response"]):
            print("  Status:", ln)
