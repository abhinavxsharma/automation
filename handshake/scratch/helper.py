import sys
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
        pg.goto(TASK_URL, timeout=30000)
        time.sleep(2)
        
    # Dismiss modal if open
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=1500):
        start_btn.click()
        time.sleep(1)
        
    return ctx, pg
