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

    # 1. Check timer modal if any
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer modal...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Check Distractor #1 value
    d1_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return { error: "No Distractor #1 label found" };
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return {
            lines: card.innerText.split('\\n').map(s => s.trim()).filter(Boolean),
            hasInput: !!card.querySelector('textarea, input'),
            inputVal: card.querySelector('textarea, input')?.value || null
        };
    }""")
    print("Distractor #1 state:", d1_info)

    # 3. Check feedback sidebar
    sidebar_info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const bannerLine = bodyText.split('\\n').find(l => l.includes('sent back') || l.includes('Distractor'));
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        // Find Science Judge card buttons
        const sjCard = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('Science Judge - Lumiere') && e.children.length > 2);
        let sjButtons = [];
        if (sjCard) {
            sjButtons = Array.from(sjCard.querySelectorAll('button')).map(b => ({
                aria: b.getAttribute('aria-label'),
                title: b.getAttribute('title'),
                text: b.innerText.trim(),
                rect: b.getBoundingClientRect()
            }));
        }

        return {
            bannerLine,
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? { text: nextBtn.innerText.trim(), disabled: nextBtn.disabled, rect: nextBtn.getBoundingClientRect() } : null,
            submitBtn: submitBtn ? { text: submitBtn.innerText.trim(), disabled: submitBtn.disabled } : null,
            sjButtons
        };
    }""")
    print("Sidebar state:\n", json.dumps(sidebar_info, indent=2))

    page.screenshot(path="scratch/current_resume_state.png")
    print("Saved scratch/current_resume_state.png")
