import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Click the Continue button
    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue with radio selected...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_error_type_advancing.png")
    print("Screenshot saved to scratch/after_error_type_advancing.png")
