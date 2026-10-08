import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # Dismiss timer if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 1. Scroll Distractor #1 into view
    found_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!d1) return { error: "No Distractor #1 label found" };

        let card = d1;
        for (let i = 0; i < 4; i++) {
            if (card.parentElement) card = card.parentElement;
        }

        card.scrollIntoView({ behavior: 'instant', block: 'center' });

        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        const btns = Array.from(card.querySelectorAll('button')).map(b => ({
            aria: b.getAttribute('aria-label'),
            text: b.innerText.trim(),
            rect: b.getBoundingClientRect()
        }));

        return {
            text: card.innerText.replace(/\\n/g, ' '),
            cardRect: card.getBoundingClientRect(),
            hasEditBtn: !!editBtn,
            btns: btns
        };
    }""")
    print("Distractor #1 card info before click:", found_info)

    # 2. Click the edit button on Distractor #1
    page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = d1;
        for (let i = 0; i < 4; i++) {
            if (card.parentElement) card = card.parentElement;
        }
        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        if (editBtn) editBtn.click();
    }""")
    page.wait_for_timeout(1000)

    # 3. Inspect the card after clicking edit
    after_edit = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = d1;
        for (let i = 0; i < 4; i++) {
            if (card.parentElement) card = card.parentElement;
        }
        const ta = card.querySelector('textarea, input[type="text"]');
        const btns = Array.from(card.querySelectorAll('button')).map(b => ({
            aria: b.getAttribute('aria-label'),
            text: b.innerText.trim(),
            html: b.outerHTML.substring(0, 100),
            rect: b.getBoundingClientRect()
        }));
        return {
            cardText: card.innerText.replace(/\\n/g, ' '),
            hasTa: !!ta,
            taVal: ta ? ta.value : null,
            btns: btns
        };
    }""")
    print("Distractor #1 card info after click edit:", after_edit)

    page.screenshot(path="scratch/d1_edit_opened.png")
    print("Saved d1_edit_opened.png")
