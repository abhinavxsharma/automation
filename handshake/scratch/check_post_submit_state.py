import sys
import time

sys.path.append("handshake/scratch")
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    page.screenshot(path="handshake/scratch/current_post_submit_state.png")
    print("Saved current_post_submit_state.png")

    # Check text inside Step 7
    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())

    # Check top status bar
    saved_indicator = page.locator(
        "text='Changes saved', text='Unsaved changes'"
    ).all()
    for s in saved_indicator:
        print("Status indicator:", s.inner_text())

    # Check if any dialog or modal is open
    modals = page.locator(
        "div[role='dialog'], div[role='alertdialog'], div[class*='modal']"
    ).all()
    print("Modals found:", len(modals))
    for m in modals:
        print("Modal text:", m.inner_text()[:200])

    # Check buttons inside editor
    spinners = page.locator("svg[class*='spin'], [class*='loading']").all()
    print("Spinners found:", len(spinners))
