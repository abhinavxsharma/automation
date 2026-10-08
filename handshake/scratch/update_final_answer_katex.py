import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_selector("button:has-text('Save'), button:has-text('Start timer')", timeout=15000)
    page.wait_for_timeout(1000)

    # 1. Dismiss timer modal
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Dismissing Start timer...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # 2. Cancel any open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    # 3. Update Final Answer (Edit button 9)
    print("\n--- Updating Final Answer to $(A+B)C$ ---")
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    fa_btn = edit_btns[9]
    fa_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    fa_btn.click()
    page.wait_for_timeout(1000)

    # Find the input or textarea in Final Answer card
    fa_input = page.locator("textarea, input[type='text']").first
    print("Old Final Answer:", repr(fa_input.input_value()))
    fa_input.fill("$(A+B)C$")
    page.wait_for_timeout(500)
    print("New Final Answer:", repr(fa_input.input_value()))

    # Click Submit on Final Answer card
    submitted = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return false;
        const sub = cancelBtn.parentElement.querySelector("button[aria-label='Submit']");
        if (sub) {
            sub.click();
            return true;
        }
        return false;
    }""")
    print("Final Answer submitted:", submitted)
    page.wait_for_timeout(2000)

    # 4. Verify Final Answer display
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    fa_card_text = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const btn = editBtns[9];
        let card = btn.parentElement;
        while (card && !card.getAttribute('data-block-id') && !card.classList.contains('border') && card !== document.body) {
            card = card.parentElement;
        }
        return {
            hasKaTeX: !!card.querySelector('.katex'),
            text: card.innerText.trim().replace(/\\n+/g, ' ')
        };
    }""")
    print("Final Answer after update:", fa_card_text)

    page.screenshot(path="handshake/scratch/after_fa_updated.png")
    print("Saved screenshot to handshake/scratch/after_fa_updated.png")
