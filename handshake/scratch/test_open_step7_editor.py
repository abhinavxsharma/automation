import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Cancel any currently open editor
    cancel_btn = page.locator("button:has-text('Cancel')").first
    if cancel_btn.is_visible(timeout=1000):
        print("Canceling current editor...")
        cancel_btn.click(force=True)
        time.sleep(1)

    # Find the edit button for Step 7
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons: {len(edit_btns)}")
    
    # Step 7 is edit_btns[7]
    prompt_btn = edit_btns[7]
    prompt_btn.scroll_into_view_if_needed()
    time.sleep(0.5)
    print("Clicking Edit on Step 7...")
    prompt_btn.click(force=True)
    time.sleep(2)

    page.screenshot(path="scratch/step7_open_editor.png")
    print("Screenshot saved to scratch/step7_open_editor.png")

    # Inspect visible buttons and textareas in editor
    for b in page.locator("button").all():
        if b.is_visible():
            txt = b.inner_text().strip().replace('\n', ' ')
            aria = b.get_attribute("aria-label") or ""
            if txt or aria:
                print(f"  Button: txt='{txt}' aria='{aria}'")

    for ta in page.locator("textarea").all():
        if ta.is_visible():
            print(f"  Textarea value: {ta.input_value()[:100]}...")
