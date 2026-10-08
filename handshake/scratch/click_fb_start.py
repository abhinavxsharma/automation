import sys
import time

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    _, pg = get_task_page(p)
    time.sleep(1)

    start_btn = pg.locator("button:has-text('Start')").first
    print("Start button visible?", start_btn.is_visible())
    if start_btn.is_visible():
        start_btn.click(force=True)
        time.sleep(2)

    pg.screenshot(path="scratch/feedback_start_clicked.png")
    print("Saved scratch/feedback_start_clicked.png")
