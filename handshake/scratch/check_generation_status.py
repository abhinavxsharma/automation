import sys
import time

from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    for _ in range(20):
        text = page.evaluate("() => document.body ? document.body.innerText : ''")
        if "Block" in text or "Generation" in text or "Algorithms" in text:
            break
        time.sleep(0.5)

    full_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in full_text.splitlines() if ln.strip()]

    print("--- Live Task Status ---")
    capture = False
    for ln in lines:
        if "Block 1" in ln:
            capture = True
        if capture:
            print(f"  {ln}")

    page.screenshot(path="scratch/live_generation_view.png")
    print("Saved scratch/live_generation_view.png")
