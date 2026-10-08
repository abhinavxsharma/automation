import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    cbs = page.locator("label:has-text('Block 1 - Response 1'), label:has-text('Block 2 - Response 1')").all()
    print(f"Found {len(cbs)} checkboxes for model failure identification.")
    for cb in cbs:
        print(f"Clicking: {cb.inner_text()}")
        cb.click(force=True)
        time.sleep(0.3)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_failure_id_continue.png")
    print("Screenshot saved to scratch/after_failure_id_continue.png")
