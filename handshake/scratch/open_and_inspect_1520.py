import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    ctx = browser.contexts[0]
    print(f"Total pages: {len(ctx.pages)}")
    for i, pg in enumerate(ctx.pages):
        print(f"Page {i}: {pg.url}")
    
    # Target 1520c7f4
    page_1520 = next((pg for pg in ctx.pages if "1520c7f4" in pg.url), None)
    if not page_1520:
        print("Page 1520c7f4 not found among tabs, opening it...")
        page_1520 = ctx.new_page()
        page_1520.goto("https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run")
    else:
        print("Page 1520c7f4 found, bringing to front...")
        page_1520.bring_to_front()
    
    page_1520.wait_for_timeout(3000)
    page_1520.screenshot(path="scratch/live_1520_inspect.png")
    print("URL:", page_1520.url)
    txt = page_1520.evaluate("() => document.body ? document.body.innerText : ''")
    Path("scratch/live_1520_text.txt").write_text(txt, encoding="utf-8")
    print("Text length:", len(txt))
    print("Preview:\n", txt[:500])
