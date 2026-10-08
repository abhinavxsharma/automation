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

    # Dismiss timer modal via JS
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Let's inspect the feedback sidebar tabs and buttons
    info = page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('button'));
        const disagreeBtns = allBtns.filter(b => b.getAttribute('aria-label') === 'Disagree');
        
        return {
            disagreeCount: disagreeBtns.length,
            buttons: disagreeBtns.map((b, i) => {
                let card = b.closest('.rounded-rosetta-container') || b.parentElement;
                return {
                    i,
                    cardText: card ? card.innerText.slice(0, 100).replace(/\\n+/g, ' ') : null
                };
            })
        };
    }""")
    print("Disagree buttons info:\n", json.dumps(info, indent=2))
