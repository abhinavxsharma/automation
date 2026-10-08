import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Find Distractor #1 element and its card text
    d1_data = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return { error: "No Distractor #1 label found" };

        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        card.scrollIntoView({ behavior: 'instant', block: 'center' });

        return {
            lines: card.innerText.split('\\n').map(s => s.trim()).filter(Boolean),
            hasInput: !!card.querySelector('textarea, input'),
            inputVal: card.querySelector('textarea, input')?.value || null,
            editBtn: !!card.querySelector('button[aria-label="Edit this step"]')
        };
    }""")
    print("D1 Data:", d1_data)
    page.screenshot(path="scratch/d1_scrolled_view.png")
    print("Saved scratch/d1_scrolled_view.png")
