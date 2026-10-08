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

    loc = page.locator("text=Image Description Checker").first
    print("Locator visible:", loc.is_visible())
    if loc.is_visible():
        box = loc.bounding_box()
        print("Bounding box:", box)

    # Check button 'Start'
    s_btn = page.locator("button:has-text('Start')").first
    print("Start button count:", page.locator("button:has-text('Start')").count())
    if s_btn.count() > 0:
        print("Start button visible:", s_btn.is_visible(), "enabled:", s_btn.is_enabled(), "box:", s_btn.bounding_box())
        print("Start button outerHTML:", s_btn.evaluate("el => el.outerHTML"))

    # Check if there is an ignore/dismiss icon or button
    # In the screenshot, next to Image Description Checker - Lumiere there is an icon
    ignore_icons = page.locator("[class*='finding'], [class*='sidebar'], aside").locator("button, svg").all()
    print("Icons in sidebar count:", len(ignore_icons))
