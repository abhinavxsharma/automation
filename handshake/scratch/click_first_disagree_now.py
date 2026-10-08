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

    # Click first Disagree button via JS
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
        if (btns.length === 0) return { error: 'No Disagree buttons' };
        
        btns[0].click();
        return { clicked: true, total: btns.length };
    }""")
    print("Clicked first Disagree:", res)
    page.wait_for_timeout(1000)

    # Inspect what appeared
    info = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea\");
        if (!ta) return { error: 'No textarea' };
        
        // Find all buttons in the same container or card
        let p = ta.parentElement;
        while (p && p.querySelectorAll('button').length < 2 && p !== document.body) {
            p = p.parentElement;
        }
        
        const btns = p ? Array.from(p.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            outerHTML: b.outerHTML,
            visible: b.offsetWidth > 0
        })) : [];

        return {
            taPlaceholder: ta.placeholder,
            taValue: ta.value,
            btns,
            containerHTML: p ? p.innerHTML.slice(0, 1000) : null
        };
    }""")
    print("After click info:\n", json.dumps(info, indent=2))
    page.screenshot(path="handshake/scratch/disagree_form_inspected.png")
