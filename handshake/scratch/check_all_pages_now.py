import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    browser, page = get_task_page(p)
    print("Total contexts:", len(browser.contexts))
    for ctx_idx, ctx in enumerate(browser.contexts):
        print(f"Context {ctx_idx} pages: {len(ctx.pages)}")
        for pg_idx, pg in enumerate(ctx.pages):
            print(f"  Page {pg_idx}: url={pg.url}, title={pg.title()}")
            try:
                body_len = pg.evaluate("() => document.body ? document.body.innerText.length : 0")
                print(f"    body_len={body_len}")
            except Exception as e:
                print(f"    error evaluating: {e}")
