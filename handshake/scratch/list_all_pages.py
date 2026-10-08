import sys

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    print(f"Contexts: {len(browser.contexts)}")
    for ci, ctx in enumerate(browser.contexts):
        print(f" Context {ci}: {len(ctx.pages)} pages")
        for pi, pg in enumerate(ctx.pages):
            print(f"   Page {pi}: url='{pg.url}' title='{pg.title()}'")
