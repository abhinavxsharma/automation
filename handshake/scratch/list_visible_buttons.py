import sys
sys.stdout.reconfigure(encoding="utf-8")
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
    info = pg.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, i) => {
            const rect = b.getBoundingClientRect();
            return {
                i,
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                x: Math.round(rect.x),
                y: Math.round(rect.y),
                w: Math.round(rect.width),
                h: Math.round(rect.height)
            };
        }).filter(b => b.w > 0 && b.h > 0);
    }""")
    for b in info:
        print(f"[{b['i']:2d}] at ({b['x']}, {b['y']}): text='{b['text']}' aria='{b['aria']}'")
