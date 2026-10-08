import sys
sys.path.insert(0, ".")
import time
from pathlib import Path
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"

with sync_playwright() as p:
    ctx = create_browser_context(p)
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
        
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Clicking edit button 7...")
    edit_btns[7].scroll_into_view_if_needed()
    time.sleep(0.5)
    edit_btns[7].click(force=True)
    time.sleep(1.5)
    
    pg.screenshot(path="scratch/step7_opened.png")
    
    # Check elements inside step 7
    remove_btn = pg.locator("button[aria-label='Remove']").all()
    upload_btn = pg.locator("button[aria-label='Upload files'], input[type='file']").all()
    print(f"Remove buttons: {len(remove_btn)}, Upload elements: {len(upload_btn)}")
    
    # Check cancel or submit button
    sub_btn = pg.locator("button[aria-label='Submit'], button:has-text('Save'), button:has-text('Continue')").all()
    print("Action buttons:", [b.inner_text() or b.get_attribute("aria-label") for b in sub_btn])
