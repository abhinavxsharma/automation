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

    # 1. Dismiss timer modal if present
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # 2. Find and click Submit task button
    sub = page.locator("button:has-text('Submit task')").first
    print("Submit task visible:", sub.is_visible(), "enabled:", sub.is_enabled())
    if sub.is_visible() and sub.is_enabled():
        print("Clicking 'Submit task'...")
        sub.click()
        page.wait_for_timeout(3000)

    # 3. Check if confirmation modal appeared (e.g. Confirm submit / Logged time / Yes)
    confirm_btn = page.locator("button:has-text('Confirm'), button:has-text('Yes, submit'), button:has-text('Submit anyway')")
    if confirm_btn.count() > 0 and confirm_btn.first.is_visible():
        print(f"Confirmation modal detected! Clicking '{confirm_btn.first.inner_text()}'...")
        confirm_btn.first.click()
        page.wait_for_timeout(3000)

    page.screenshot(path="scratch/after_submit_clicked.png")
    print("Saved scratch/after_submit_clicked.png")

    body_text = page.evaluate("() => document.body ? document.body.innerText : ''")
    lines = [ln.strip() for ln in body_text.splitlines() if ln.strip()]
    print("\n--- Last 30 lines of page text ---")
    for ln in lines[-30:]:
        print(" ", ln)
