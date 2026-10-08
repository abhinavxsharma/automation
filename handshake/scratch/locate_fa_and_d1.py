import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss timer if visible
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing timer...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # Locate Distractor #1, Final Answer, etc.
    res = page.evaluate("""() => {
        const matches = [];
        const all = Array.from(document.querySelectorAll('*'));
        for (const el of all) {
            const txt = el.innerText ? el.innerText.trim() : '';
            if (txt.includes('Distractor #1') && el.children.length === 0) {
                let p = el;
                for (let i = 0; i < 4; i++) if (p.parentElement) p = p.parentElement;
                matches.push({
                    leafText: txt,
                    leafTag: el.tagName,
                    cardText: p.innerText.replace(/\\n/g, ' '),
                    hasTextarea: !!p.querySelector('textarea, input'),
                    textareaVal: p.querySelector('textarea, input')?.value || null,
                    editBtn: !!p.querySelector('button[aria-label="Edit this step"]')
                });
            }
        }
        return matches;
    }""")
    for m in res:
        print(f"Leaf text: {m['leafText']}")
        print(f"Has textarea: {m['hasTextarea']}, val: {m['textareaVal']}, editBtn: {m['editBtn']}")
        print(f"Card preview: {m['cardText'][:100]}...")
