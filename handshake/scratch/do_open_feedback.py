import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

with sync_playwright() as p:
    b, page = get_task_page(p)
    page.wait_for_selector("button[aria-label='Feedback']", timeout=10000)
    btn = page.locator("button[aria-label='Feedback']").first
    btn.click()
    page.wait_for_timeout(2000)
    page.screenshot(path="scratch/feedback_opened_now.png")
    print("Clicked Feedback button!")
