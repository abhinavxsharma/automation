import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(2000)

    # Dismiss timer if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Cancel any open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print(f"Total edit_btns: {len(edit_btns)}")

    # Distractor 1 is edit_btns[18]
    d1_btn = edit_btns[18]
    d1_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    d1_btn.click()
    page.wait_for_timeout(1000)

    # Fill target value
    ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
    target_val = r"$(A+\overline{B})C$"
    ta.fill(target_val)
    page.wait_for_timeout(500)

    # Find the submit button next to Cancel
    submit_btn = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return false;
        const sub = cancelBtn.parentElement.querySelector("button[aria-label='Submit']");
        if (sub) {
            sub.click();
            return true;
        }
        return false;
    }""")
    print("Submit button clicked via JS:", submit_btn)
    page.wait_for_timeout(2000)

    # Take screenshot of Distractor 1 card
    page.screenshot(path="handshake/scratch/d1_after_commit.png")
    print("Screenshot saved to handshake/scratch/d1_after_commit.png")
