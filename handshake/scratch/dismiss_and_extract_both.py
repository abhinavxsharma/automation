import sys
import time

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Wait for page hydration
    for _ in range(20):
        t = page.evaluate("() => document.body ? document.body.innerText : ''")
        if len(t) > 200:
            break
        time.sleep(0.5)

    # Click Start timer if modal is present
    btn = page.locator("button:has-text('Start timer')").first
    box = btn.bounding_box()
    if box:
        print(f"Clicking Start timer at ({box['x'] + box['width']/2}, {box['y'] + box['height']/2})...")
        page.mouse.click(box["x"] + box["width"]/2, box["y"] + box["height"]/2)
        page.wait_for_timeout(1000)

    # Scroll all the way down
    for _ in range(6):
        page.evaluate("() => { if (document.body) window.scrollTo(0, document.body.scrollHeight); }")
        page.wait_for_timeout(400)

    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/full_page_both_models_text.txt", "w", encoding="utf-8") as f:
        f.write(full_text)

    print("=== SEARCHING FOR MODEL ANSWERS ===")
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]
    for i, ln in enumerate(lines):
        if "Block 1" in ln or "Block 2" in ln or "Final Answer" in ln or "boxed" in ln.lower():
            # print surrounding context
            context = " | ".join(lines[max(0, i-2):min(len(lines), i+8)])
            print(f"Match [{ln}]: {context[:180]}")

    page.screenshot(path="scratch/live_page_after_both.png")
    print("Screenshot saved to scratch/live_page_after_both.png")
