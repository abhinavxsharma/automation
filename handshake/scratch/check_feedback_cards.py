import sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    page.wait_for_timeout(2000)
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Inspect the cards inside the Feedback sidebar
    cards_info = page.evaluate("""() => {
        const side = document.querySelector("[data-testid='task-side-panel'], div.w-80");
        if (!side) return 'NO_SIDEBAR';
        const items = Array.from(side.querySelectorAll("div.border, div.rounded-lg, div[class*='card']")).filter(el => el.innerText.includes('Finding number'));
        return items.map((card, i) => {
            const btns = Array.from(card.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                aria: b.getAttribute('aria-label'),
                className: b.className
            }));
            return {
                index: i,
                text: card.innerText.trim().replace(/\\n+/g, ' | '),
                buttons: btns
            };
        });
    }""")
    print("Feedback Cards Info:\n", cards_info)
