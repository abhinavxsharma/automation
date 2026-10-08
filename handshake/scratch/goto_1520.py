import sys
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

target = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"

with sync_playwright() as p:
    ensure_chrome()
    b = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = b.contexts[0].pages[0]
    print("Navigating to:", target)
    page.goto(target, wait_until="domcontentloaded")
    page.wait_for_timeout(4000)
    print("Navigated. Current URL:", page.url)
    page.screenshot(path="scratch/live_1520_ready.png")
