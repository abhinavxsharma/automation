import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Check for any dialog in the DOM right now
    dialog_info = page.evaluate("""() => {
        const dialog = document.querySelector("div[role='dialog']");
        if (!dialog) return null;
        return {
            id: dialog.id,
            className: dialog.className,
            text: dialog.innerText,
            buttons: Array.from(dialog.querySelectorAll('button')).map(b => ({
                text: b.innerText,
                aria: b.getAttribute('aria-label')
            }))
        };
    }""")
    print("Dialog info:", dialog_info)
    page.screenshot(path="handshake/scratch/intercepting_dialog.png")
    print("Screenshot saved to handshake/scratch/intercepting_dialog.png")
