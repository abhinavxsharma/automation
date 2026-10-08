import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer if visible
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)

    # Audit all form fields
    audit = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        
        // Find Distractors
        const distractors = [];
        for (let i = 1; i <= 5; i++) {
            const label = 'Distractor #' + i + ':';
            const all = Array.from(document.querySelectorAll('*'));
            const el = all.find(e => e.innerText && e.innerText.trim() === label && e.children.length === 0);
            if (el) {
                let card = el;
                for (let k = 0; k < 4; k++) if (card.parentElement) card = card.parentElement;
                const lines = card.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
                distractors.push({ label, lines, full: card.innerText.replace(/\\n/g, ' ') });
            }
        }

        // Find Final Answer
        const faEl = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.trim() === 'Final Answer:' && e.children.length === 0);
        let faCard = null;
        if (faEl) {
            let card = faEl;
            for (let k = 0; k < 4; k++) if (card.parentElement) card = card.parentElement;
            faCard = card.innerText.replace(/\\n/g, ' ');
        }

        // Check banner
        const bannerLine = bodyText.split('\\n').find(l => l.includes('sent back') || l.includes('Distractor'));

        // Check sidebar
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');

        return {
            bannerLine,
            distractors,
            finalAnswer: faCard,
            counter: counter ? counter[0] : null,
            submitBtn: submitBtn ? {
                text: submitBtn.innerText.trim(),
                disabled: submitBtn.disabled,
                classes: submitBtn.className
            } : null
        };
    }""")

    print(json.dumps(audit, indent=2))
