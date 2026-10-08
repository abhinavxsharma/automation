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

    # Targets for distractors 2 to 5
    # Distractor 1 is already $(A+\overline{B})C$
    # Distractor 2: $C$
    # Distractor 3: $A+BC$
    # Distractor 4: $AC$
    # Distractor 5: $AB+C$
    targets = {
        19: "$C$",
        20: "$A+BC$",
        21: "$AC$",
        22: "$AB+C$"
    }

    for idx, target_val in targets.items():
        print(f"\n--- Updating Distractor {idx - 17} to {target_val} ---")
        btns = page.locator("button").all()
        edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
        btn = edit_btns[idx]
        btn.scroll_into_view_if_needed()
        page.wait_for_timeout(500)
        btn.click()
        page.wait_for_timeout(1000)

        ta = page.locator("textarea[placeholder='Plausible-but-wrong answer text']").first
        print("Previous value:", repr(ta.input_value()))
        ta.fill(target_val)
        page.wait_for_timeout(500)

        # Click Submit
        clicked = page.evaluate("""() => {
            const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
            if (!cancelBtn) return false;
            const sub = cancelBtn.parentElement.querySelector("button[aria-label='Submit']");
            if (sub) {
                sub.click();
                return true;
            }
            return false;
        }""")
        print("Submit clicked:", clicked)
        page.wait_for_timeout(2000)

    # Take screenshot of distractors
    page.screenshot(path="handshake/scratch/all_distractors_updated.png")
    print("\nScreenshot saved to handshake/scratch/all_distractors_updated.png")
