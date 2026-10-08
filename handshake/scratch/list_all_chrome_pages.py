import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    print(f"Contexts count: {len(browser.contexts)}")
    for c_idx, ctx in enumerate(browser.contexts):
        print(f"Context {c_idx} pages count: {len(ctx.pages)}")
        for p_idx, pg in enumerate(ctx.pages):
            print(f"  Page {p_idx}: URL={pg.url}, Title={pg.title()}")
