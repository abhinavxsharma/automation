import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"

def get_page(playwright):
    ctx = create_browser_context(playwright)
    pg = next((t for t in ctx.pages if "/task/" in t.url), None)
    if not pg:
        pg = ctx.pages[0] if ctx.pages else ctx.new_page()
        pg.goto(TASK_URL)
        pg.wait_for_load_state("networkidle")
        time.sleep(2)
        
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=2000):
        start_btn.click(force=True)
        time.sleep(1)
        
    return ctx, pg

with sync_playwright() as p:
    ctx, pg = get_page(p)
    file_btns = pg.locator("button[aria-label*='View file']").all()
    print("View file buttons:", [b.get_attribute("aria-label") for b in file_btns])
    
    # Also check any img src in the main page
    imgs = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('img')).map(i => ({
            src: i.src.slice(0, 100),
            alt: i.alt,
            width: i.naturalWidth,
            height: i.naturalHeight
        }));
    }""")
    print("Images on page:", imgs)
