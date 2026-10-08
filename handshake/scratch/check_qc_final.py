import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_timeout(3000)
    side = page.locator("[data-testid='task-side-panel'], div.w-80").first
    print("Sidebar text:\n", side.inner_text() if side.count() > 0 else "NO SIDEBAR")
    page.screenshot(path="handshake/scratch/qc_after_all_distractors.png")
