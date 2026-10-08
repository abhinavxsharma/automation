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

    # 1. Dismiss modal
    page.evaluate("""() => {
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Click Disagree button on Science Judge (btns[1])
    clicked = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
        if (btns[1]) {
            btns[1].click();
            return true;
        }
        return false;
    }""")
    print("Clicked Science Judge Disagree button:", clicked)
    page.wait_for_timeout(1500)

    # 3. Inspect Science Judge card HTML
    card_html = page.evaluate("""() => {
        const allCards = Array.from(document.querySelectorAll(\"div.rounded-rosetta-container\"));
        const sjCard = allCards.find(c => c.innerText && c.innerText.includes('Science Judge'));
        return sjCard ? sjCard.innerHTML : 'No SJ card found';
    }""")
    print("Science Judge card HTML length:", len(card_html))
    print("Preview of SJ card HTML:\n", card_html[-1500:])
