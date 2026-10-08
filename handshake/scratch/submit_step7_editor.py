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
    
    # Find submit button (up arrow) in the active editor
    submit_btn = pg.locator("button[aria-label='Submit'], button:has(svg path[d*='M5 10l7-7m0 0l7 7m-7-7v18']), button:has(svg)").filter(has=pg.locator("svg")).last
    print("Clicking submit button...")
    
    # Try finding the up-arrow button specifically next to Cancel
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible():
        parent = cancel_btn.locator("xpath=..")
        up_btn = parent.locator("button").last
        print("Clicking up_btn next to cancel...")
        up_btn.click(force=True)
    else:
        submit_btn.click(force=True)
        
    time.sleep(3)
    pg.screenshot(path="scratch/after_submit_step7.png")
    print("Saved screenshot: scratch/after_submit_step7.png")
    
    # Check what is currently visible on page
    dialog = pg.locator("[role='dialog']").all()
    print("Dialogs:", len(dialog))
    for d in dialog:
        print("Dialog text:", d.inner_text().replace('\n', ' ')[:200])
        
    checkboxes = pg.locator("input[type='checkbox'], label:has(input[type='checkbox'])").all()
    print("Checkboxes found:", len(checkboxes))
    for cb in checkboxes:
        print("Checkbox:", cb.inner_text().replace('\n', ' ')[:100])
        
    cont_btn = pg.locator("button:has-text('Continue')").all()
    print("Continue buttons:", len(cont_btn))
