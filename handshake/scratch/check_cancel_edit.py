import sys
sys.path.insert(0, ".")
import time
from handshake_automation.browser import create_browser_context
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = create_browser_context(p)
    pg = next((t for t in ctx.pages if "/task/" in t.url), ctx.pages[0])
    
    # Check if Cancel button is visible
    cancel_btn = pg.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible():
        print("Clicking Cancel...")
        cancel_btn.click()
        time.sleep(1)
        
    edit_btns = pg.locator("button[aria-label='Edit this step']").all()
    print("Edit buttons after cancel:", len(edit_btns))
