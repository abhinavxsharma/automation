import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

REASON = (
    "The prompt explicitly instructs to determine the fully simplified Boolean expression for output Q "
    "in terms of inputs A, B, and C from the provided circuit image, and to return the final answer as a single "
    "Boolean expression for Q using standard Boolean notation. The required output Q and simplification "
    "are completely and unambiguously defined from the prompt and the provided circuit topology."
)


def handle_modals(page):
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Dismissing Start timer modal...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    rt_btn = page.locator("button[aria-label='Resume timer']")
    if rt_btn.count() > 0 and rt_btn.first.is_visible():
        print("Clicking Resume timer...")
        rt_btn.first.click()
        page.wait_for_timeout(1000)


ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)
    page.wait_for_timeout(1000)

    handle_modals(page)

    # Cancel any lingering editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    # Find edit buttons
    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    print("Found edit buttons:", len(edit_btns))
    target_btn = edit_btns[23]
    target_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)

    handle_modals(page)
    target_btn.click()
    page.wait_for_timeout(1000)

    # If start timer modal popped up right after click, dismiss and click again
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        st_btn.first.click()
        page.wait_for_timeout(1000)
        target_btn.click()
        page.wait_for_timeout(1000)

    ta = page.locator("textarea").first
    print(f"Step 23 old value: {repr(ta.input_value())}")
    ta.fill(REASON)
    page.wait_for_timeout(500)
    print(f"Step 23 new value: {repr(ta.input_value()[:50])}")

    submitted = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return false;
        const sub = cancelBtn.parentElement.querySelector(\"button[aria-label='Submit']\");
        if (sub) {
            sub.click();
            return true;
        }
        return false;
    }""")
    print("Submitted Step 23:", submitted)
    page.wait_for_timeout(2000)

    # Click top-bar Save button
    top_saved = page.evaluate("""() => {
        const topSave = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (topSave && !topSave.disabled) {
            topSave.click();
            return true;
        }
        return false;
    }""")
    print("Clicked top Save:", top_saved)
    page.wait_for_timeout(1500)

    # Verify Step 23 card text
    step23_text = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        const b23 = btns[23];
        let card = b23 ? (b23.closest('[data-block-id]') || b23.parentElement) : null;
        return card ? card.innerText : 'None';
    }""")
    print("\n--- STEP 23 VERIFIED TEXT ---\n", step23_text)

    page.screenshot(path="handshake/scratch/step23_final_verified.png")
    print("Saved screenshot to handshake/scratch/step23_final_verified.png")
