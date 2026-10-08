import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    int_opt = page.locator("label:has-text('Integer'), [role='radio']:has-text('Integer'), input[value='Integer']").first
    print("Selecting Integer...")
    int_opt.click(force=True)
    time.sleep(0.5)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_answer_format_continue.png")
    print("Screenshot saved to scratch/after_answer_format_continue.png")
