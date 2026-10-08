import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # 1. Dismiss modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Clicking Start timer...")
        modal_btn.first.click()
        page.wait_for_timeout(1000)

    # 2. Inspect element at (970, 210)
    el_info = page.evaluate("""() => {
        const el = document.elementFromPoint(970, 210);
        if (!el) return null;
        const btn = el.closest('button') || el;
        return {
            tag: btn.tagName,
            aria: btn.getAttribute('aria-label'),
            title: btn.getAttribute('title'),
            classes: btn.className,
            rect: btn.getBoundingClientRect()
        };
    }""")
    print("Element at (970, 210):", el_info)

    # Click at (970, 210)
    print("Clicking at (970, 210)...")
    page.mouse.click(970, 210)
    page.wait_for_timeout(1500)

    page.screenshot(path="scratch/after_click_ignore_icon.png")
    print("Saved scratch/after_click_ignore_icon.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln)
