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
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Dismissing Start timer...")
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Find Distractor #1 card and its edit button
    print("Finding Distractor #1 edit button...")
    edit_btn_box = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return null;

        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        card.scrollIntoView({ behavior: 'instant', block: 'center' });

        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        if (editBtn) {
            const r = editBtn.getBoundingClientRect();
            return { x: r.x, y: r.y, width: r.width, height: r.height };
        }
        return null;
    }""")
    print("Edit button box:", edit_btn_box)

    if not edit_btn_box:
        print("Error: Edit button not found")
        sys.exit(1)

    # Click the edit button
    page.mouse.click(edit_btn_box["x"] + edit_btn_box["width"] / 2, edit_btn_box["y"] + edit_btn_box["height"] / 2)
    page.wait_for_timeout(1500)

    # 3. Check for input/textarea in the card
    card_open_info = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;

        const ta = card.querySelector('textarea, input[type="text"]');
        const cancelBtn = Array.from(card.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        
        let commitBtnBox = null;
        if (cancelBtn) {
            const siblingBtns = Array.from(cancelBtn.parentElement.querySelectorAll('button')).filter(b => b !== cancelBtn);
            if (siblingBtns.length > 0) {
                const r = siblingBtns[0].getBoundingClientRect();
                commitBtnBox = { x: r.x, y: r.y, width: r.width, height: r.height };
            }
        }

        let taBox = null;
        if (ta) {
            const r = ta.getBoundingClientRect();
            taBox = { x: r.x, y: r.y, width: r.width, height: r.height };
        }

        return {
            hasTa: !!ta,
            currVal: ta ? ta.value : null,
            taBox: taBox,
            hasCancel: !!cancelBtn,
            commitBtnBox: commitBtnBox
        };
    }""")
    print("Card open info:", card_open_info)

    page.screenshot(path="scratch/d1_opened_step.png")

    # 4. Fill 85 into textarea
    if card_open_info.get("hasTa"):
        print("Filling 85 into input...")
        # Use both JS React property descriptor and Playwright typing to be 100% sure
        page.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'));
            const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
            let card = el;
            for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
            const ta = card.querySelector('textarea, input[type="text"]');
            if (ta) {
                const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                               Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
                if (setVal) setVal.call(ta, '85');
                else ta.value = '85';
                ta.dispatchEvent(new Event('input', { bubbles: true }));
                ta.dispatchEvent(new Event('change', { bubbles: true }));
            }
        }""")
        page.wait_for_timeout(500)

        # 5. Click the commit button
        cbox = card_open_info.get("commitBtnBox")
        if cbox:
            print(f"Clicking commit button at ({cbox['x'] + cbox['width']/2}, {cbox['y'] + cbox['height']/2})...")
            page.mouse.click(cbox["x"] + cbox["width"] / 2, cbox["y"] + cbox["height"] / 2)
            page.wait_for_timeout(1500)

    # 6. Click top Save
    save_btn = page.locator("button:has-text('Save')").first
    if save_btn.is_visible():
        print("Clicking top Save...")
        save_btn.click()
        page.wait_for_timeout(2500)

    # 7. Check verified state
    verified = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return {
            lines: card.innerText.split('\\n').map(s => s.trim()).filter(Boolean),
            hasInput: !!card.querySelector('textarea, input')
        };
    }""")
    print("Verified Distractor #1:", verified)

    page.screenshot(path="scratch/after_d1_commit_and_save.png")
    print("Saved scratch/after_d1_commit_and_save.png")
