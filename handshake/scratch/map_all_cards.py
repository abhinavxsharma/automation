import sys
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Find all edit buttons
    cards_info = page.evaluate("""() => {
        const editBtns = Array.from(document.querySelectorAll("button[aria-label='Edit this step']"));
        return editBtns.map((btn, idx) => {
            // Find container card
            let el = btn.parentElement;
            while (el && !el.getAttribute('data-block-id') && el.tagName !== 'SECTION' && !el.classList.contains('border') && el !== document.body) {
                el = el.parentElement;
            }
            const text = el ? el.innerText : '';
            const firstLines = text.split('\\n').map(l => l.trim()).filter(Boolean).slice(0, 3).join(' | ');
            return {
                idx: idx,
                summary: firstLines,
                fullLength: text.length
            };
        });
    }""")

    print(f"Found {len(cards_info)} cards:")
    for c in cards_info:
        print(f"Card {c['idx']}: {c['summary']} (len: {c['fullLength']})")
