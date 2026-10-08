import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    dialog_info = page.evaluate("""() => {
        const dialog = document.querySelector(\"[role='dialog']\");
        if (!dialog) return { error: 'No dialog' };
        
        const btns = Array.from(dialog.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0,
            classes: b.className
        }));
        
        return {
            text: dialog.innerText,
            btns
        };
    }""")
    print("Dialog info:\n", json.dumps(dialog_info, indent=2))
