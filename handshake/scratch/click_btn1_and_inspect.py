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
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Click button 1
    click_res = page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('button'));
        const disagreeBtns = allBtns.filter(b => b.getAttribute('aria-label') === 'Disagree');
        if (disagreeBtns[1]) {
            disagreeBtns[1].click();
            return { clicked: true };
        }
        return { clicked: false, count: disagreeBtns.length };
    }""")
    print("Click result:", click_res)
    page.wait_for_timeout(1500)

    # 3. Inspect what appeared
    card_info = page.evaluate("""() => {
        const allCards = Array.from(document.querySelectorAll(\"div.rounded-rosetta-container\"));
        const sjCard = allCards.find(c => c.innerText && c.innerText.includes('Science Judge'));
        if (!sjCard) return { error: 'No SJ card found' };

        const textareas = Array.from(sjCard.querySelectorAll('textarea, input')).map(t => ({
            tag: t.tagName,
            placeholder: t.placeholder,
            value: t.value
        }));
        
        const buttons = Array.from(sjCard.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            outerHTML: b.outerHTML
        }));

        return {
            textareas,
            buttons,
            cardText: sjCard.innerText
        };
    }""")
    print("SJ Card Info after clicking Disagree:\n", json.dumps(card_info, indent=2))
    page.screenshot(path="handshake/scratch/sj_card_after_click_inspect.png")
