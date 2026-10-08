import sys
sys.stdout.reconfigure(encoding="utf-8")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Let's inspect the buttons near Cancel in the editor
    cancel_btn = page.locator("button:has-text('Cancel')").first
    if not cancel_btn.is_visible():
        print("Cancel button not visible - editor may not be open!")
        # Let's take a screenshot
        page.screenshot(path="scratch/current_screen_now.png")
        sys.exit(0)

    print("Found Cancel button.")
    parent = cancel_btn.locator("xpath=..")
    buttons = parent.locator("button").all()
    print(f"Buttons inside Cancel's parent container: {len(buttons)}")
    for i, b in enumerate(buttons):
        tag = b.evaluate("e => e.tagName")
        txt = b.inner_text().strip()
        aria = b.get_attribute("aria-label") or ""
        cls = b.get_attribute("class") or ""
        dis = b.is_disabled()
        html = b.evaluate("e => e.outerHTML")
        print(f"  [{i}] tag={tag} text='{txt}' aria='{aria}' disabled={dis}")
        print(f"       HTML: {html}")
