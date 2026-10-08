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

    # 1. Dismiss timer modal
    modal_btn = page.locator("button:has-text('Start timer')")
    if modal_btn.count() > 0 and modal_btn.first.is_visible():
        print("Dismissing timer modal...")
        modal_btn.first.click()
        page.wait_for_timeout(500)

    # 2. Check if feedback sidebar is open
    sidebar_visible = page.locator("text=Needs attention").is_visible()
    print("Feedback sidebar visible:", sidebar_visible)
    if not sidebar_visible:
        # Click the feedback toggle button in top bar (the one with the checkmark icon)
        toggle = page.locator("button:has(svg path[d*='M20.25 6'])").or_(page.locator("button[aria-label*='feedback']")).or_(page.locator("header button").nth(4))
        print("Clicking feedback toggle...")
        # Coordinate of toggle button in top bar: x=862, y=24
        page.mouse.click(862, 24)
        page.wait_for_timeout(1000)
        sidebar_visible = page.locator("text=Needs attention").is_visible()
        print("After click, feedback sidebar visible:", sidebar_visible)

    # 3. Check what is in the feedback sidebar
    if sidebar_visible:
        sidebar_text = page.locator("aside, [class*='sidebar'], div:has(> button:has-text('Needs attention'))").first.inner_text()
        print("\n--- Feedback Sidebar Text ---")
        print(sidebar_text)

    # 4. Scroll to Submit task button
    sub = page.locator("button:has-text('Submit task')")
    print("\nSubmit task button count:", sub.count())
    if sub.count() > 0:
        sub_btn = sub.first
        print("Submit button visible:", sub_btn.is_visible(), "enabled:", sub_btn.is_enabled())
        # Scroll it into view
        sub_btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)

    page.screenshot(path="scratch/submit_screen_ready.png")
    print("Saved scratch/submit_screen_ready.png")
