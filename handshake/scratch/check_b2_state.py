import sys
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
from helper import get_page
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    ctx, pg = get_page(p)
    pg.reload()
    time.sleep(4)
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=2000):
        start_btn.click()
        time.sleep(1)
        
    pg.evaluate("() => { const el = document.getElementById('task-scroll-container'); if (el) el.scrollTop = el.scrollHeight; }")
    text = pg.evaluate("() => document.body ? document.body.innerText : ''")
    idx = text.find("Block 2 Responses:")
    if idx != -1:
        snippet = text[idx:idx+400]
        print("B2 snippet:\n", snippet.encode('ascii', 'replace').decode('ascii'))
        print("Still generating?", "Generating response" in snippet)
        if "Generating response" not in snippet:
            print("\n>>> BLOCK 2 COMPLETED! <<<")
            cont = pg.locator("button:has-text('Continue')").first
            print("Continue button visible?", cont.is_visible())
    else:
        print("Block 2 not found")
