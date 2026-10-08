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

    # Inspect textarea and sibling buttons
    res = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
        if (!ta) return { error: 'No textarea' };
        
        let p = ta.parentElement;
        const btns = Array.from(p.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0,
            classes: b.className
        }));
        
        return {
            taPlaceholder: ta.placeholder,
            parentHTML: p.innerHTML.slice(0, 500),
            btns
        };
    }""")
    print("Disagree input & buttons:\n", json.dumps(res, indent=2))
