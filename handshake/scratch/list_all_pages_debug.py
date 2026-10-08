import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    pages = browser.contexts[0].pages
    print(f"Total pages: {len(pages)}")
    for i, pg in enumerate(pages):
        print(f"Page {i}: URL={pg.url}, Title={pg.title()}")
        # Check if 1520c is in url
        if "1520c" in pg.url or "task" in pg.url:
            print(f"  Body text preview: {pg.inner_text('body')[:300]!r}")
