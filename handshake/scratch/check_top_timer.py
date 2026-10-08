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

    # Let's inspect the top bar buttons
    top_btns = page.evaluate("""() => {
        const header = document.querySelector('header') || document.querySelector('nav') || document.body;
        return Array.from(document.querySelectorAll('button')).slice(0, 15).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            className: b.className
        }));
    }""")
    print("Top buttons:")
    for b in top_btns:
        print(" ", b)
