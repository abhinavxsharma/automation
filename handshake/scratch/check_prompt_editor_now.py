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
    page.wait_for_timeout(2000)

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        print("Clicking Start timer...")
        st_btn.first.click()
        page.wait_for_timeout(1000)

    # Cancel any open editor
    cancel_btn = page.locator("button:has-text('Cancel')")
    if cancel_btn.count() > 0 and cancel_btn.first.is_visible():
        cancel_btn.first.click()
        page.wait_for_timeout(1000)

    # Let's inspect all edit buttons
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    print(f"Total edit buttons: {len(edit_btns)}")
    
    # Prompt is button 7
    prompt_btn = edit_btns[7]
    prompt_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    prompt_btn.click()
    page.wait_for_timeout(1000)

    # Inspect what opened
    info = page.evaluate("""() => {
        const dialog = document.querySelector("[role='dialog'], [role='alertdialog']");
        const ta = document.querySelector("textarea");
        const callouts = Array.from(document.querySelectorAll("div.border, div[class*='callout'], div[class*='alert'], [role='alert']")).map(el => el.innerText.trim()).filter(Boolean);
        return {
            hasDialog: !!dialog,
            dialogText: dialog ? dialog.innerText : null,
            hasTextarea: !!ta,
            textareaVal: ta ? ta.value : null,
            callouts: callouts.slice(0, 5)
        };
    }""")
    print("Prompt Edit Info:\n", info)

    page.screenshot(path="handshake/scratch/prompt_edit_inspect_now.png")
    print("Screenshot saved to handshake/scratch/prompt_edit_inspect_now.png")
