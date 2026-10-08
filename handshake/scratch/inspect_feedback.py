import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    fb = pg.locator("text='Prompt Checker - Lumiere'").first
    print("Feedback visible?", fb.is_visible())

    start_btn = pg.locator("button:has-text('Start')").first
    print("Start button visible?", start_btn.is_visible())
    if start_btn.is_visible():
        print("Start button outerHTML:", start_btn.evaluate("el => el.outerHTML"))

    # Also inspect Block 1 Responses
    block1 = pg.locator("text='Block 1 Responses:'").first
    print("Block 1 visible?", block1.is_visible())
    if block1.is_visible():
        print("Block 1 parent HTML:", block1.evaluate("el => el.parentElement.outerHTML")[:500])
