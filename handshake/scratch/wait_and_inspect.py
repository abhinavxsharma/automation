import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    print("Waiting for skeleton to disappear and content to load...")
    for i in range(20):
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Final Answer" in text or "Algorithms" in text:
            print(f"Content ready after {i * 0.5}s! Text length: {len(text)}")
            break
        time.sleep(0.5)

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=2000):
        st_btn.click()
        page.wait_for_timeout(1000)
        print("Dismissed timer modal.")

    # Now let's inspect the active card / textarea / input for Final Answer
    ta = page.locator("textarea").first
    inp = page.locator("input:not([type='hidden'])").first
    print("Textarea visible:", ta.is_visible())
    if ta.is_visible():
        print("Textarea placeholder:", ta.get_attribute("placeholder"))
    print("Input visible:", inp.is_visible())
    if inp.is_visible():
        print("Input placeholder:", inp.get_attribute("placeholder"))

    # Also find Continue button
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Continue button visible:", cont_btn.is_visible())
