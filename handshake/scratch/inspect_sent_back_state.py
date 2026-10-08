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
    page.wait_for_timeout(1000)

    # Dismiss timer modal if present
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0:
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(500)

    # 1. Distractor #1 info
    d1_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return { error: "Distractor #1 not found" };
        let p = el;
        for (let i = 0; i < 4; i++) if (p.parentElement) p = p.parentElement;
        const editBtn = p.querySelector('button[aria-label="Edit this step"]');
        return {
            cardText: p.innerText.replace(/\\n/g, ' '),
            hasEditBtn: !!editBtn
        };
    }""")
    print("Distractor #1:", d1_info)

    # 2. Science Judge in Feedback panel
    sj_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length === 0);
        if (!el) return { error: "Science Judge finding not found" };
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        const btns = Array.from(card.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label') || '',
            html: b.outerHTML.slice(0, 100),
            rect: b.getBoundingClientRect()
        }));
        return {
            cardText: card.innerText.replace(/\\n/g, ' '),
            buttons: btns
        };
    }""")
    print("\nScience Judge in sidebar:", json.dumps(sj_info, indent=2))

    # 3. Sidebar counter and action buttons
    sidebar_info = page.evaluate("""() => {
        const body = document.body.innerText;
        const m = body.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextOrSubmit = Array.from(document.querySelectorAll('button')).find(b => {
            const t = b.innerText.trim();
            return (t === 'Next' || t === 'Submit task' || t === 'Start') && b.getBoundingClientRect().x > 700;
        });
        return {
            counter: m ? m[0] : 'Not found',
            actionBtn: nextOrSubmit ? {
                text: nextOrSubmit.innerText.trim(),
                disabled: nextOrSubmit.disabled,
                rect: nextOrSubmit.getBoundingClientRect()
            } : null
        };
    }""")
    print("\nSidebar status:", sidebar_info)

    page.screenshot(path="scratch/sent_back_inspected.png")
