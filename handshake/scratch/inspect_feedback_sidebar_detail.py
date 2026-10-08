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
    
    # Check the sidebar cards
    resolve_btns = pg.locator("button[aria-label='Resolve']").all()
    print("Resolve checkmark buttons:", len(resolve_btns))
    for i, b in enumerate(resolve_btns):
        print(f"Resolve btn {i}: at ({b.bounding_box()})")
        
    # Check input fields in the feedback sidebar
    inputs = pg.locator("aside input, aside textarea, div[data-testid*='feedback'] input").all()
    print("Inputs in sidebar:", len(inputs))
    for i, inp in enumerate(inputs):
        print(f"Input {i}: placeholder='{inp.get_attribute('placeholder')}' value='{inp.input_value()}'")
        
    pg.screenshot(path="scratch/feedback_sidebar_detail.png")
