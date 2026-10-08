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

    # Let's inspect the Prompt card (Edit 7)
    btns = page.locator("button").all()
    edit_btns = [b for b in btns if b.get_attribute("aria-label") == "Edit this step"]
    prompt_btn = edit_btns[7]

    card_info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        const btn = editBtns[7];
        let el = btn.parentElement;
        while (el && !el.getAttribute('data-block-id') && !el.classList.contains('border') && el !== document.body) {
            el = el.parentElement;
        }
        return {
            blockId: el.getAttribute('data-block-id'),
            classes: el.className,
            text: el.innerText
        };
    }""")
    print("Prompt Card Info:", card_info)
