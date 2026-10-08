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
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Found edit buttons:", len(edit_btns))
    for i, b in enumerate(edit_btns):
        txt = b.evaluate("el => el.closest('div.flex-col, div[data-block-id], section')?.innerText || ''")
        first_line = txt.strip().splitlines()[0] if txt.strip() else 'EMPTY'
        print(f"{i:2d}: {first_line[:60]}")
        
    pg.screenshot(path="scratch/current_9_steps.png")
    
    # Check bottom buttons like Continue or Next
    btns = pg.locator("button:has-text('Continue'), button:has-text('Next'), button:has-text('Submit')").all()
    print("Action buttons:", [b.inner_text() for b in btns])
    
    # Check any unchecked checkboxes
    cbs = pg.locator("input[type='checkbox']").all()
    print("Checkboxes count:", len(cbs))
    for cb in cbs:
        print("CB checked:", cb.is_checked())
