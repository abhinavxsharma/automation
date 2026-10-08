import sys
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, ".")
sys.path.insert(0, "scratch")
import time
from helper import get_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx, pg = get_page(p)
    cont_btn = pg.locator("button:has-text('Continue')").first
    print("Clicking Continue button...")
    cont_btn.click(force=True)
    time.sleep(3)
    
    pg.screenshot(path="scratch/after_editor_continue_clean.png")
    
    # Check visible buttons
    btns = pg.locator("button:has-text('Next'), button:has-text('Submit task'), button:has-text('Submit')").all()
    print("Action buttons:", [b.inner_text() for b in btns])
    
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Total edit buttons now:", len(edit_btns))
