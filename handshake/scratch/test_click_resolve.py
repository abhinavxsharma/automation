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
    
    resolve_btns = pg.locator("button[aria-label='Resolve']").all()
    print("Clicking resolve button 0...")
    resolve_btns[0].click(force=True)
    time.sleep(1.5)
    
    pg.screenshot(path="scratch/after_click_resolve_0.png")
    
    # Check if a textarea or input opened
    inputs = pg.locator("textarea, input[type='text']").all()
    print("Total text inputs now:", len(inputs))
    for inp in inputs:
        print("Input:", inp.get_attribute("placeholder"), inp.bounding_box())
        
    airplane = pg.locator("button:has(svg path[d*='M2.01 21L23 12 2.01 3 2 10l15 2-15 2z']), button.rosetta-button:has(svg)").all()
    print("Paper airplane buttons:", len(airplane))
