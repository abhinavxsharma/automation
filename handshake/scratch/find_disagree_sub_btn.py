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

    # Inspect textarea in sidebar and find its submit button
    btn_info = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
        if (!ta) return { error: 'No textarea' };
        
        let container = ta.parentElement;
        while (container && container.querySelectorAll('button').length === 0 && container !== document.body) {
            container = container.parentElement;
        }
        
        const btns = container ? Array.from(container.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0,
            classes: b.className
        })) : [];
        
        // Also look at next siblings
        let sib = ta.nextElementSibling;
        let sibs = [];
        while (sib) {
            sibs.push({ tag: sib.tagName, text: sib.innerText, html: sib.outerHTML.slice(0, 200) });
            sib = sib.nextElementSibling;
        }

        return {
            containerHTML: container ? container.outerHTML.slice(0, 800) : null,
            btns,
            sibs
        };
    }""")
    print("Submit button info:\n", json.dumps(btn_info, indent=2))
