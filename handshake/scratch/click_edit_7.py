import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(20):
        if "Final Answer" in page.evaluate("() => document.body ? document.body.innerText : ''"):
            break
        time.sleep(0.5)

    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print("Clicking edit_btns[7]...")
    edit_btns[7].scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    edit_btns[7].click(force=True)
    page.wait_for_timeout(2000)

    page.screenshot(path="scratch/clicked_edit_btn7.png")
    print("Screenshot saved to scratch/clicked_edit_btn7.png")

    # Check if a modal or textarea opened
    modals = page.locator("div[role='dialog'], [role='alertdialog']").all()
    print(f"Modals open: {len(modals)}")
    for m in modals:
        print("  Modal text:", m.inner_text()[:200])

    # Check if textarea is visible now
    ta = page.locator("textarea").all()
    print(f"Textareas found: {len(ta)}")
    for t in ta:
        print("  Textarea:", t.is_visible(), t.input_value()[:100])
