import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Dismissing Start timer modal...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    submit_btn = page.locator("button:has-text('Submit task')").first
    print("Clicking Submit task button...")
    submit_btn.click()
    page.wait_for_timeout(2000)

    # Check for confirmation dialog
    dialog = page.locator("div[role='dialog'], div[role='alertdialog']").first
    if dialog.count() > 0 and dialog.is_visible():
        print("\nConfirmation dialog appeared:")
        print(dialog.inner_text())
        
        # Look for confirm / submit button inside dialog
        conf_btns = dialog.locator("button").all()
        for cb in conf_btns:
            txt = cb.inner_text().strip()
            print(f"  Dialog button: '{txt}'")
            if any(w in txt.lower() for w in ['submit', 'confirm', 'yes', 'proceed', 'finish']):
                print(f"Clicking confirmation button: '{txt}'")
                cb.click()
                break
        page.wait_for_timeout(3000)

    # Wait for page update after submission
    page.wait_for_timeout(3000)
    page.screenshot(path="handshake/scratch/after_submit_task_clicked.png")
    print("\nSaved screenshot to handshake/scratch/after_submit_task_clicked.png")
    print("Current URL:", page.url)
    print("Page Title:", page.title())
    
    # Inspect body text snippet
    body_txt = page.locator("body").inner_text()[:600].replace('\n', ' ')
    print("Body text snippet:\n", body_txt)
