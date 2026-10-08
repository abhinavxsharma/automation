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

    # Inspect Golden Solution (Edit 16)
    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    gs_card = edit_btns[16].evaluate("el => el.closest('div.border, section, [data-block-id]').innerText")
    
    # Print the distractor section of Golden Solution
    print("Golden Solution distractor section:")
    for line in gs_card.split("\n"):
        if "Distractor" in line or "distractor" in line.lower() or "Rationale" in line:
            print(line)
