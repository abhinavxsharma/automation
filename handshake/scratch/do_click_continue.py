import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for page hydration
    for _ in range(20):
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Click continue" in text or "Algorithms" in text:
            print("Page hydrated!")
            break
        time.sleep(0.5)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Find Continue button
    cont_btn = page.locator("button:has-text('Continue'), button[aria-label='Continue']").last
    if cont_btn.is_visible(timeout=5000):
        print("Found Continue button! Clicking...")
        cont_btn.click(force=True)
        page.wait_for_timeout(3000)
    else:
        print("Continue button still not visible after hydration.")

    page.screenshot(path="scratch/after_continue_clicked_fresh.png")
    print("Saved scratch/after_continue_clicked_fresh.png")

    # Read text
    text_now = page.evaluate("() => document.body ? document.body.innerText : ''")
    for ln in text_now.splitlines():
        if any(w in ln for w in ["Generating", "Block", "response", "Responses"]):
            print("  Status:", ln)
