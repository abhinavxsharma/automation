import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss modals
    for sel in ["button:has-text('Start timer')", "button:has-text('Got it')", "button:has-text('OK')"]:
        btn = page.locator(sel).first
        if btn.is_visible(timeout=500):
            btn.click(force=True)
            page.wait_for_timeout(500)

    # Click Submit button inside the prompt editor
    sub_btn = page.locator("button:has-text('Submit')").first
    if sub_btn.is_visible():
        print("Found Submit button! Clicking it...")
        sub_btn.click(force=True)
        page.wait_for_timeout(2000)
    else:
        print("Submit button not found by text! Searching aria-label...")
        sub_btn = page.locator("button[aria-label='Submit']").first
        if sub_btn.is_visible():
            sub_btn.click(force=True)
            page.wait_for_timeout(2000)

    page.screenshot(path="scratch/after_submit_click_v2.png")
    print("Saved scratch/after_submit_click_v2.png")

    # Check for confirmation dialog or checkboxes
    modals = page.locator("div[role='dialog'], [role='alertdialog']").all()
    print(f"Modals open: {len(modals)}")
    for m in modals:
        print("Modal text:", m.inner_text()[:200])

    # Check for Continue button
    cont_btn = page.locator("button:has-text('Continue')").first
    if cont_btn.is_visible(timeout=1000):
        print("Found Continue button! Clicking it...")
        cont_btn.click(force=True)
        page.wait_for_timeout(2000)
        page.screenshot(path="scratch/after_continue_click_v2.png")
        print("Saved scratch/after_continue_click_v2.png")
