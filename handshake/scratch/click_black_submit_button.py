import sys
sys.stdout.reconfigure(encoding="utf-8")
import time
from chrome_helper import get_task_page
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser, page = get_task_page(p)

    # Find the black Submit button
    sub_btns = page.locator("button:has-text('Submit')").all()
    print(f"Found {len(sub_btns)} buttons with text 'Submit':")
    for i, b in enumerate(sub_btns):
        print(f"  [{i}] visible={b.is_visible()} text='{b.inner_text()}' aria='{b.get_attribute('aria-label')}' class='{b.get_attribute('class')}'")

    target_btn = next((b for b in sub_btns if b.is_visible()), None)
    if target_btn:
        print("Clicking visible Submit button...")
        target_btn.click(force=True)
        time.sleep(3)
        page.screenshot(path="scratch/after_clicking_black_submit.png")
        print("Screenshot saved to scratch/after_clicking_black_submit.png")

        # Check for any confirmation modal
        dialogs = page.locator("div[role='dialog'], [role='alertdialog']").all()
        print(f"Dialogs found: {len(dialogs)}")
        for i, d in enumerate(dialogs):
            print(f"Dialog {i} text: {d.inner_text()[:200]}")
            # Look for Confirm, Continue, Proceed, or Submit button
            confirm_btn = d.locator("button:has-text('Continue'), button:has-text('Confirm'), button:has-text('Delete'), button:has-text('Submit')").first
            if confirm_btn.is_visible(timeout=1000):
                print(f"Clicking confirm button in dialog: {confirm_btn.inner_text()}")
                confirm_btn.click(force=True)
                time.sleep(2)
                page.screenshot(path="scratch/after_confirming_modal.png")
    else:
        print("No visible Submit button found!")
