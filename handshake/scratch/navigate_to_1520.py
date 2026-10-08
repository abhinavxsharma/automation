import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    
    target_url = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
    if "1520c7f4" not in page.url:
        print(f"Navigating page 0 from {page.url} to {target_url}...")
        page.goto(target_url)
    
    page.wait_for_timeout(3000)
    page.screenshot(path="scratch/live_1520_persisted.png")
    
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/live_1520_text.txt").write_text(txt, encoding="utf-8")
    print("Page URL:", page.url)
    print("Text length:", len(txt))
    print("Screenshot saved to scratch/live_1520_persisted.png")
