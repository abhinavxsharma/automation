import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss timer modal
    dismissed = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) {
            st.click();
            return 'Dismissed timer modal';
        }
        return 'No timer modal';
    }""")
    print("Modal dismiss:", dismissed)
    page.wait_for_timeout(1000)

    # 2. Check the Science Judge card and sidebar buttons
    sb_info = page.evaluate("""() => {
        const sjCard = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 1);
        
        const allBtns = Array.from(document.querySelectorAll('button')).map((b, idx) => ({
            idx,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            classes: b.className,
            rect: b.getBoundingClientRect()
        })).filter(b => b.rect.x > 700);

        return {
            hasSjCard: !!sjCard,
            sjCardText: sjCard ? sjCard.innerText.replace(/\\n/g, ' ') : null,
            sidebarButtons: allBtns
        };
    }""")
    print("Sidebar info:\n", json.dumps(sb_info, indent=2))

    # 3. Let's see what happens if we click 'Next' button
    next_click = page.evaluate("""() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        if (nextBtn) {
            nextBtn.click();
            return 'Clicked Next button';
        }
        return 'No Next button found';
    }""")
    print("Next click attempt:", next_click)
    page.wait_for_timeout(1500)

    # 4. Check status after clicking Next
    after_next = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const sub = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        const next = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        return {
            counter: counter ? counter[0] : null,
            hasSubmitTask: !!sub,
            hasNext: !!next,
            sidebarText: bodyText.slice(bodyText.indexOf('Feedback'))
        };
    }""")
    print("Status after Next:\n", json.dumps(after_next, indent=2))

    page.screenshot(path="scratch/after_next_click.png")
    print("Saved scratch/after_next_click.png")
