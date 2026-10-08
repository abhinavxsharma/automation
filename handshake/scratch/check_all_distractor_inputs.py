import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(2000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Cancel any open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    
    # Check distractors 1 to 5 (indices 18, 19, 20, 21, 22)
    for i in range(18, 23):
        btn = edit_btns[i]
        btn.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        btn.click()
        page.wait_for_timeout(500)
        ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
        val = ta.input_value()
        print(f"Distractor #{i-17} raw input value: {repr(val)}")
        c_btn = page.locator("button:has-text('Cancel')").first
        c_btn.click()
        page.wait_for_timeout(500)
        # re-query edit buttons
        btns = page.locator("button").all()
        edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
