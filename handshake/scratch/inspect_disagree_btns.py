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

    # Let's inspect buttons with aria-label='Disagree'
    disagree_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
        return btns.map((b, i) => {
            let card = b.parentElement;
            while (card && !card.innerText.includes('Science Judge') && card !== document.body) {
                card = card.parentElement;
            }
            return {
                i,
                visible: b.offsetWidth > 0,
                parentCardText: card ? card.innerText.slice(0, 300).replace(/\\n+/g, ' ') : 'None'
            };
        });
    }""")
    print("Disagree buttons info:\n", json.dumps(disagree_info, indent=2))
