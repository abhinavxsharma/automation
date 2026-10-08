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
        print("Dismissing timer modal...")
        page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        page.wait_for_timeout(500)

    # Select Connectivity / topology error
    opt = page.locator("label:has-text('Connectivity / topology error'), div:has-text('Connectivity / topology error')").first
    print("Selecting Connectivity / topology error...")
    opt.click(force=True)
    page.wait_for_timeout(500)

    # Click Continue
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_topology_select.png")
    print("Saved scratch/after_topology_select.png")

    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    print("\n--- Active Step Context ---")
    for ln in lines[-35:]:
        print(" ", ln)
