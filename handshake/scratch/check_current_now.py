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

    page.screenshot(path="scratch/current_now.png")
    print("Saved scratch/current_now.png")
    txt = page.evaluate("() => document.body ? document.body.innerText : ''")
    print("Page innerText length:", len(txt))
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    for ln in lines[-35:]:
        print(" ", ln)
