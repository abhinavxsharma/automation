import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
import time
from pathlib import Path
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

TASK_URL = "https://ai.joinhandshake.com/annotations/fellow/task/1520c7f4-d41f-440b-b341-e7c6bc96166c/run"
NEW_DIAGRAM = str(Path("scratch/dag_crystal_clear_v3.png").resolve())

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
    
    # 1. Open Step 7 if not open
    ta = pg.locator("textarea").first
    if not ta.is_visible():
        edit_btns = pg.locator("button[aria-label='Edit this step']").all()
        print("Clicking edit button 7...")
        edit_btns[7].scroll_into_view_if_needed()
        time.sleep(0.5)
        edit_btns[7].click(force=True)
        time.sleep(1.5)
        
    # 2. Check remove button
    rem_btn = pg.locator("button[aria-label='Remove']").first
    if rem_btn.is_visible(timeout=2000):
        print("Clicking remove button on old image...")
        rem_btn.click(force=True)
        time.sleep(1)
        
    pg.screenshot(path="scratch/after_remove_old_img.png")
    
    # 3. Check upload button
    upload_btn = pg.locator("button[aria-label='Upload files'], button:has-text('+')").first
    print("Uploading new diagram:", NEW_DIAGRAM)
    with pg.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc = fc_info.value
    fc.set_files(NEW_DIAGRAM)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_upload_new_img.png")
    print("New diagram uploaded! Checked screenshot: scratch/after_upload_new_img.png")
