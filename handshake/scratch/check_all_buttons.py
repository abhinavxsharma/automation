import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for content
    for _ in range(20):
        if "Final Answer" in page.evaluate("() => document.body ? document.body.innerText : ''"):
            break
        time.sleep(0.5)

    # Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Let's inspect all buttons with pencil or edit
    btns = page.locator("button").all()
    print(f"Total buttons on page: {len(btns)}")
    for i, b in enumerate(btns):
        txt = b.inner_text().strip()
        aria = b.get_attribute("aria-label") or ""
        box = b.bounding_box()
        # Check if button contains svg
        has_svg = b.locator("svg").count() > 0
        if aria or has_svg or txt:
            print(f"  Btn {i}: text='{txt}' aria='{aria}' has_svg={has_svg} box={box}")
