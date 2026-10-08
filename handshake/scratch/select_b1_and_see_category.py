import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Click Block 1 - Response 1 radio
    b1_radio = page.locator("label:has-text('Block 1 - Response 1')").first
    print("Selecting Block 1 - Response 1...")
    b1_radio.click(force=True)
    page.wait_for_timeout(500)

    # Click Continue
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_pick_b1.png")
    print("Saved scratch/after_pick_b1.png")

    new_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in new_text.splitlines() if ln.strip()]
    print("\n--- Active Step After Picking B1 ---")
    for ln in lines[-35:]:
        print(" ", ln)
