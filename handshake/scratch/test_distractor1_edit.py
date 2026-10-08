import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print(f"Total edit_btns: {len(edit_btns)}")

    # Let's inspect Distractor 1 (index 18)
    d1_btn = edit_btns[18]
    print("Clicking Edit this step on Distractor 1...")
    d1_btn.click()
    page.wait_for_timeout(1000)

    # Check what appears (inputs, textareas, buttons)
    inputs = page.locator("input, textarea").all()
    print(f"Inputs found: {len(inputs)}")
    for inp in inputs:
        if inp.is_visible():
            val = inp.input_value()
            tag = inp.evaluate("el => el.tagName")
            placeholder = inp.get_attribute("placeholder") or ""
            print(f"Visible {tag}: val='{val}' placeholder='{placeholder}'")

    page.screenshot(path="handshake/scratch/distractor1_edit_open.png")
    print("Screenshot saved to handshake/scratch/distractor1_edit_open.png")
