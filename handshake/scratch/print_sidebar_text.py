import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # Let's inspect sidebar text
    bodyText = page.evaluate("() => document.body.innerText")
    fbIdx = bodyText.find("Feedback")
    if fbIdx != -1:
        print("Feedback sidebar text:\n", bodyText[fbIdx:fbIdx + 1200])
