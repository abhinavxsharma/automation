import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Click Edit on Prompt card (index 7)
    edit_btns = page.locator("button[aria-label='Edit this step']").all()
    prompt_btn = edit_btns[7]
    prompt_btn.scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    prompt_btn.click()
    page.wait_for_timeout(1000)

    ta = page.locator("textarea").first
    print("Textarea visible:", ta.is_visible())
    
    # Check if there is an onBlur, onChange, or top save
    save_btn = page.locator("button:has-text('Save')").first
    print("Top save button enabled:", save_btn.is_enabled())

    page.screenshot(path="handshake/scratch/prompt_editor_active.png")

    # Cancel for now to keep state clean
    cancel_btn = page.locator("button:has-text('Cancel')").first
    cancel_btn.click()
    page.wait_for_timeout(1000)
