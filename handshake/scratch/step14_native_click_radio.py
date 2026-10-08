import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    radio = page.locator("input[type='radio'][value='0']").first
    radio.scroll_into_view_if_needed()
    time.sleep(0.5)
    print("Clicking radio natively with Playwright...")
    radio.click(force=True)
    time.sleep(1)

    cont_btn = page.locator("button:has-text('Continue')").first
    print("Clicking Continue...")
    cont_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/after_native_radio_click.png")
    print("Screenshot saved to scratch/after_native_radio_click.png")
