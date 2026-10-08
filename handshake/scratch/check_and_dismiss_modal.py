import sys
sys.path.insert(0, ".")
import time
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
    
    # Dismiss / start timer modal if visible
    start_btn = pg.locator("button:has-text('Start timer')").first
    if start_btn.is_visible(timeout=3000):
        print("Clicking Start timer...")
        start_btn.click(force=True)
        time.sleep(2)
        
    pg.screenshot(path="scratch/after_dismiss_timer_1520.png")
    print("Page Title:", pg.title())
    print("Page URL:", pg.url)
