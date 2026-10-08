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
    print("Page ready:", pg.title())
    
    # 1. Cancel any open editor first
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible(timeout=1000):
        print("Canceling current editor...")
        cancel_btn.click(force=True)
        time.sleep(1)
        
    # 2. Find and click Edit button for Step 7
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Clicking Edit on Step 7 (button 7)...")
    edit_btns[7].scroll_into_view_if_needed()
    time.sleep(0.5)
    edit_btns[7].click(force=True)
    time.sleep(2)
    
    # 3. Wait for textarea to be visible
    ta = pg.locator("textarea").first
    ta.wait_for(state="visible", timeout=5000)
    print("Step 7 editor is open!")
    
    # 4. Remove old image
    rem_btn = pg.locator("button[aria-label='Remove']").first
    if rem_btn.is_visible(timeout=2000):
        print("Removing old image...")
        rem_btn.click(force=True)
        time.sleep(1.5)
    else:
        print("No remove button visible!")
        
    # 5. Upload new diagram
    upload_btn = pg.locator("button[aria-label='Upload files'], button:has-text('+')").first
    print("Uploading:", NEW_DIAGRAM)
    with pg.expect_file_chooser() as fc_info:
        upload_btn.click(force=True)
    fc = fc_info.value
    fc.set_files(NEW_DIAGRAM)
    time.sleep(3)
    
    pg.screenshot(path="scratch/step7_after_file_set.png")
    
    # 6. Click Submit (up-arrow button inside editor)
    # The submit button is in the same container as Cancel
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    parent = cancel_btn.locator("xpath=..")
    arrow_btn = parent.locator("button").last
    print("Clicking arrow submit button inside Step 7...")
    arrow_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/step7_after_submit_click.png")
    
    # Check if any modal / dialog or checkboxes appeared
    print("Checking after submit:")
    file_btns = pg.locator("button[aria-label*='View file']").all()
    for b in file_btns:
        print("Attached file:", b.get_attribute("aria-label"))
