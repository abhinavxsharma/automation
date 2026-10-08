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

    # Dismiss timer modal if present
    btn = page.locator("button:has-text('Start timer')").first
    box = btn.bounding_box()
    if box:
        page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        page.wait_for_timeout(500)

    # Check Block 1 - Response 1 checkbox
    b1_cb = page.locator("label:has-text('Block 1 - Response 1')").first
    print("Checking Block 1 - Response 1...")
    b1_cb.click(force=True)
    page.wait_for_timeout(300)

    # Check Block 2 - Response 1 checkbox
    b2_cb = page.locator("label:has-text('Block 2 - Response 1')").first
    print("Checking Block 2 - Response 1...")
    b2_cb.click(force=True)
    page.wait_for_timeout(300)

    # Click Continue
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_failure_select.png")
    print("Saved scratch/after_failure_select.png")

    new_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in new_text.splitlines() if ln.strip()]
    print("\n--- Active Step After Failure Selection ---")
    for ln in lines[-35:]:
        print(" ", ln)
