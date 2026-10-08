import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    for i in range(20):
        if page.locator("button").count() > 5:
            break
        page.wait_for_timeout(500)

    # Scroll to bottom
    page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(1000)

    # Check Submit task button
    sub = page.locator("button:has-text('Submit task')")
    print("Submit task button count:", sub.count())
    if sub.count() > 0:
        sub_btn = sub.first
        print("Submit button visible:", sub_btn.is_visible(), "enabled:", sub_btn.is_enabled())
        print("Submit button box:", sub_btn.bounding_box())

    page.screenshot(path="scratch/page_bottom.png")
    print("Saved scratch/page_bottom.png")
