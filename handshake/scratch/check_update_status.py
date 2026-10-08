from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')").first
    if st_btn.is_visible(timeout=1000):
        st_btn.click()
        page.wait_for_timeout(1000)

    # Let's inspect what text is on the page now
    text = page.evaluate("() => document.body ? document.body.innerText : ''")
    with open("scratch/current_after_update_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    # Check for any error messages or progress indicators
    print("Page text snippet (first 1000 chars):")
    print(text[:1000])

    page.screenshot(path="scratch/current_post_update.png")
    print("Saved scratch/current_post_update.png")

    # Check for statement checkboxes if they appeared
    cbs = page.locator("input[type='checkbox'], [role='checkbox'], label:has-text('double checked')").all()
    print(f"Checkboxes found: {len(cbs)}")
    for cb in cbs:
        print("  Checkbox:", cb.is_visible(), cb.is_checked() if hasattr(cb, "is_checked") else "N/A")
