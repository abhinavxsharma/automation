import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import get_task_page

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # 1. Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # 2. Click Cancel to NOT edit prompt
    cancel_btn = page.locator("button:has-text('Cancel')").first
    if cancel_btn.count() > 0 and cancel_btn.is_visible():
        print("Clicking Cancel...")
        cancel_btn.click()
        page.wait_for_timeout(1000)

    page.screenshot(path="scratch/after_cancel_edit.png")
    print("Saved scratch/after_cancel_edit.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln)
