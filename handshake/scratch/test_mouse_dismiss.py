import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    btn = page.locator("button:has-text('Start timer')").first
    print("Start timer visible:", btn.is_visible())
    if btn.is_visible():
        box = btn.bounding_box()
        print("Bounding box:", box)
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    btn_after = page.locator("button:has-text('Start timer')").first
    print("Start timer visible after click:", btn_after.is_visible())

    page.screenshot(path="scratch/modal_dismissed_proof.png")
    print("Saved scratch/modal_dismissed_proof.png")
