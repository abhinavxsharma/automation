import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    try:
        page.wait_for_selector("button:has-text('Save'), button:has-text('Start timer')", timeout=15000)
    except Exception as e:
        print("Timeout waiting for selector:", e)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    body_text = page.locator("body").inner_text()
    print("Body length:", len(body_text))
    print("Body preview:\n", body_text[:400])

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print(f"Total buttons: {len(btns)}, Edit buttons: {len(edit_btns)}")
    
    for i, b in enumerate(edit_btns):
        txt = b.evaluate("el => el.closest('div.border, section, [data-block-id]') ? el.closest('div.border, section, [data-block-id]').innerText.substring(0, 120).replace(/\\n+/g, ' ') : 'NO CONTAINER'")
        print(f"Edit {i}: {txt}")
