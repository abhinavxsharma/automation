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

    # Click 'All' in the feedback panel
    page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && e.innerText.trim() === 'All');
        if (allBtns.length > 0) allBtns[allBtns.length - 1].click();
    }""")
    page.wait_for_timeout(1000)

    # Find all buttons with aria-label='Disagree'
    disagree_btns = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
        return btns.map((b, i) => {
            let p = b.parentElement;
            let text = '';
            for (let step = 0; step < 5; step++) {
                if (p) {
                    text = p.innerText;
                    if (text.includes('Finding number') || text.includes('Science Judge')) break;
                    p = p.parentElement;
                }
            }
            return {
                i,
                visible: b.offsetWidth > 0,
                classes: b.className,
                text: text.slice(0, 300).replace(/\\n+/g, ' ')
            };
        });
    }""")
    print("Disagree buttons:\n", json.dumps(disagree_btns, indent=2))
