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

    # Scroll the main container to the bottom
    page.evaluate("""() => {
        const scrollable = Array.from(document.querySelectorAll('div')).filter(d => d.scrollHeight > d.clientHeight && d.clientHeight > 300);
        for (const s of scrollable) {
            s.scrollTop = s.scrollHeight;
        }
        window.scrollTo(0, document.body.scrollHeight);
    }""")
    page.wait_for_timeout(1000)

    # Find the Submit task button
    sub = page.locator("button:has-text('Submit task')").first
    print("Submit task button visible:", sub.is_visible(), "enabled:", sub.is_enabled())
    print("Submit button box:", sub.bounding_box())

    page.screenshot(path="scratch/final_submit_view.png")
    print("Saved scratch/final_submit_view.png")
