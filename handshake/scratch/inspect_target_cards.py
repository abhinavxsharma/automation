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

    # Inspect Final Answer (Edit 9)
    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print(f"Total edit_btns: {len(edit_btns)}")
    if len(edit_btns) < 24:
        page.wait_for_timeout(2000)
        btns = page.locator("button").all()
        edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
        print(f"After retry: {len(edit_btns)}")

    print("--- Final Answer Card (Edit 9) ---")
    fa_card = edit_btns[9].evaluate("el => el.closest('div.border, section, [data-block-id]').innerText")
    print(fa_card)

    print("\n--- Distractor Cards (Edit 18-22) ---")
    for i in range(18, 23):
        d_card = edit_btns[i].evaluate("el => el.closest('div.border, section, [data-block-id]').innerText")
        print(f"\nDistractor {i-17}:\n{d_card}")

    print("\n--- Prompt Card (Edit 7) ---")
    p_card = edit_btns[7].evaluate("el => el.closest('div.border, section, [data-block-id]').innerText")
    print(p_card)
