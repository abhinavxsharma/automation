import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # 2. Inspect Distractor #1 section
    distractor_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!d1) return { error: "Distractor #1 not found" };

        let c = d1;
        let btn = null;
        for (let i = 0; i < 10; i++) {
            if (!c) break;
            btn = c.querySelector('button[aria-label="Edit this step"]');
            if (btn) break;
            c = c.parentElement;
        }

        return {
            containerText: c ? c.innerText.replace(/\\n/g, ' ') : '',
            hasEditBtn: !!btn
        };
    }""")
    print("Distractor #1 info:", distractor_info)

    # 3. Inspect Science Judge finding in Feedback panel
    sj_feedback_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const sjFinding = all.find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length === 0);
        if (!sjFinding) return { error: "Science Judge card not found in sidebar" };

        let card = sjFinding;
        while (card && !card.className.includes('border') && card !== document.body) {
            card = card.parentElement;
        }

        const buttons = Array.from(card.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            title: b.getAttribute('title'),
            html: b.outerHTML.slice(0, 100),
            rect: b.getBoundingClientRect()
        }));

        return {
            cardText: card.innerText.replace(/\\n/g, ' '),
            buttons
        };
    }""")
    print("\nScience Judge card in sidebar:", json.dumps(sj_feedback_info, indent=2))

    # 4. Check bottom buttons in sidebar (Next / Start / Submit)
    bottom_sidebar_info = page.evaluate("""() => {
        const body = document.body.innerText;
        const m = body.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const btns = Array.from(document.querySelectorAll('button')).filter(b => b.getBoundingClientRect().x > 700).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            rect: b.getBoundingClientRect(),
            disabled: b.disabled
        }));
        return {
            counter: m ? m[0] : 'Not found',
            buttons: btns
        };
    }""")
    print("\nSidebar bottom info:", json.dumps(bottom_sidebar_info, indent=2))
