import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss timer if visible
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        box = btn.bounding_box()
        if box:
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Toggle Feedback sidebar open if not already open
    sidebar_open = page.evaluate("""() => {
        const h = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.trim() === 'Feedback' && e.offsetWidth > 0);
        return !!h;
    }""")
    print("Sidebar open:", sidebar_open)
    if not sidebar_open:
        print("Toggling sidebar open...")
        page.mouse.click(926, 23)
        page.wait_for_timeout(1000)

    # 3. Scroll Distractor #1 into view
    print("Scrolling to Distractor #1...")
    page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (el) {
            let card = el;
            for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
            card.scrollIntoView({ behavior: 'instant', block: 'center' });
        }
    }""")
    page.wait_for_timeout(1000)

    # 4. Find the pencil edit button for Distractor #1
    edit_box = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return null;
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        const btn = card.querySelector('button[aria-label="Edit this step"]');
        if (btn) {
            const r = btn.getBoundingClientRect();
            return { x: r.x, y: r.y, width: r.width, height: r.height };
        }
        return null;
    }""")
    print("Edit box:", edit_box)
    if edit_box:
        print("Clicking edit button...")
        page.mouse.click(edit_box["x"] + edit_box["width"] / 2, edit_box["y"] + edit_box["height"] / 2)
        page.wait_for_timeout(1500)

    # 5. Check if Cancel appeared and find the input
    editor_info = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { hasCancel: false };

        let p = cancelBtn;
        while (p && !p.querySelector('textarea, input[type="text"]') && p !== document.body) {
            p = p.parentElement;
        }
        const ta = p ? p.querySelector('textarea, input[type="text"]') : null;
        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);

        return {
            hasCancel: true,
            hasTa: !!ta,
            hasCommitBtn: !!commitBtn,
            taVal: ta ? ta.value : null
        };
    }""")
    print("Editor info:", editor_info)
    page.screenshot(path="scratch/step_editor_open.png")

    # 6. Fill 85 and click commit
    if editor_info.get("hasCancel"):
        print("Filling 85 and committing...")
        page.evaluate("""() => {
            const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
            let p = cancelBtn;
            while (p && !p.querySelector('textarea, input[type="text"]') && p !== document.body) {
                p = p.parentElement;
            }
            const ta = p.querySelector('textarea, input[type="text"]');
            
            const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                           Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
            if (setVal) setVal.call(ta, '85');
            else ta.value = '85';
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));

            const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
            if (commitBtn) commitBtn.click();
        }""")
        page.wait_for_timeout(2000)

    # 7. Click top Save
    print("Clicking top Save...")
    page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) saveBtn.click();
    }""")
    page.wait_for_timeout(2500)

    # 8. Check Distractor #1 in DOM
    d1_now = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return 'Not found';
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return card.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
    }""")
    print("Distractor #1 lines now:", d1_now)

    page.screenshot(path="scratch/step_d1_committed.png")
    print("Saved scratch/step_d1_committed.png")
