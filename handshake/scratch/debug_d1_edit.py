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

    # Find the edit button for Distractor #1 and click it
    click_res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return { error: "No Distractor #1 label" };

        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        card.scrollIntoView({ behavior: 'instant', block: 'center' });

        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        if (!editBtn) return { error: "No edit button in card" };

        editBtn.click();
        return { clicked: true };
    }""")
    print("Click result:", click_res)
    page.wait_for_timeout(1500)

    # Now inspect all buttons and inputs on the page
    dom_state = page.evaluate("""() => {
        const inputs = Array.from(document.querySelectorAll('input, textarea')).map(i => ({
            tag: i.tagName,
            type: i.type,
            value: i.value,
            placeholder: i.placeholder,
            rect: i.getBoundingClientRect(),
            parentHtml: i.parentElement ? i.parentElement.outerHTML.substring(0, 100) : ''
        }));

        const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            rect: b.getBoundingClientRect(),
            html: b.outerHTML.substring(0, 100)
        })).filter(b => b.rect.width > 0 && b.rect.height > 0);

        return { inputs, buttons };
    }""")

    print(f"Visible inputs ({len(dom_state['inputs'])}):")
    for inp in dom_state['inputs']:
        print("  ", inp)

    print(f"\nVisible buttons ({len(dom_state['buttons'])}):")
    for b in dom_state['buttons']:
        if b['rect']['y'] > 200 and b['rect']['y'] < 800:
            print("  ", b)

    page.screenshot(path="scratch/debug_d1_edit.png")
    print("Saved scratch/debug_d1_edit.png")
