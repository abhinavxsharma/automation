import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(10):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if len(t) > 200:
            break
        time.sleep(0.5)

    btn = page.locator("button:has-text('Start timer')").first
    print("Is visible:", btn.is_visible())
    box = btn.bounding_box()
    print("Bounding box:", box)

    if box:
        cx = box["x"] + box["width"] / 2
        cy = box["y"] + box["height"] / 2
        print(f"Clicking at ({cx}, {cy})...")
        page.mouse.click(cx, cy)
        page.wait_for_timeout(1000)

    page.screenshot(path="scratch/after_mouse_click_timer.png")
    print("Saved scratch/after_mouse_click_timer.png")
