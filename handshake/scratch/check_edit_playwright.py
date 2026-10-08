import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print(f"Found {len(edit_btns)} edit buttons via playwright locator")
    for i, b in enumerate(edit_btns):
        txt = b.evaluate("el => el.closest('div.border, section, [data-block-id]') ? el.closest('div.border, section, [data-block-id]').innerText.substring(0, 120).replace(/\\n+/g, ' ') : 'NO CONTAINER'")
        print(f"Edit {i}: {txt}")
