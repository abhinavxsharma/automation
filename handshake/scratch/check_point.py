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

    # Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        modal_btn.first.click()
        page.wait_for_timeout(500)

    res = page.evaluate("""() => {
        const el = document.elementFromPoint(970, 210);
        if (!el) return null;
        let btn = el.closest('button') || el;
        return {
            tag: btn.tagName,
            aria: btn.getAttribute('aria-label'),
            title: btn.getAttribute('title'),
            classes: btn.className,
            outerHTML: btn.outerHTML.slice(0, 300)
        };
    }""")
    print("Element at (970, 210):", res)
