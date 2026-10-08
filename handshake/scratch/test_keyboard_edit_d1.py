import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.bring_to_front()
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss any Start timer modal
    for _ in range(3):
        btn = page.locator("button:has-text('Start timer')").first
        if btn.is_visible():
            box = btn.bounding_box()
            if box:
                print("Dismissing Start timer modal...")
                page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
                page.wait_for_timeout(800)
        else:
            break

    # 2. Scroll to Distractor #1
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
    page.wait_for_timeout(500)

    # 3. Find and click pencil button
    edit_btn = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return null;
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        const b = card.querySelector('button[aria-label="Edit this step"]');
        if (b) {
            const r = b.getBoundingClientRect();
            return { x: r.x, y: r.y, width: r.width, height: r.height };
        }
        return null;
    }""")
    print("Edit btn:", edit_btn)
    if edit_btn:
        page.mouse.click(edit_btn["x"] + edit_btn["width"] / 2, edit_btn["y"] + edit_btn["height"] / 2)
        page.wait_for_timeout(1000)

    # 4. Check if Cancel appeared
    page.screenshot(path="scratch/keyboard_editor_before_type.png")

    # 5. Find the input box and use keyboard to type 85
    inp_box = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return null;
        let p = cancelBtn;
        while (p && !p.querySelector('textarea, input[type="text"]') && p !== document.body) {
            p = p.parentElement;
        }
        const ta = p ? p.querySelector('textarea, input[type="text"]') : null;
        if (!ta) return null;
        const r = ta.getBoundingClientRect();
        return { x: r.x, y: r.y, width: r.width, height: r.height };
    }""")
    print("Input box:", inp_box)

    if inp_box:
        print("Clicking input and typing 85...")
        page.mouse.click(inp_box["x"] + inp_box["width"] / 2, inp_box["y"] + inp_box["height"] / 2)
        page.wait_for_timeout(200)
        page.keyboard.press("Control+A")
        page.wait_for_timeout(100)
        page.keyboard.press("Backspace")
        page.wait_for_timeout(100)
        page.keyboard.type("85")
        page.wait_for_timeout(500)

        # 6. Click commit button
        commit_box = page.evaluate("""() => {
            const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
            if (!cancelBtn) return null;
            const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
            if (!commitBtn) return null;
            const r = commitBtn.getBoundingClientRect();
            return { x: r.x, y: r.y, width: r.width, height: r.height };
        }""")
        print("Commit box:", commit_box)
        if commit_box:
            print("Clicking commit button with mouse...")
            page.mouse.click(commit_box["x"] + commit_box["width"] / 2, commit_box["y"] + commit_box["height"] / 2)
            page.wait_for_timeout(2000)

        # 7. Click top Save button
        save_box = page.evaluate("""() => {
            const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
            if (!saveBtn) return null;
            const r = saveBtn.getBoundingClientRect();
            return { x: r.x, y: r.y, width: r.width, height: r.height };
        }""")
        print("Save box:", save_box)
        if save_box:
            print("Clicking Save with mouse...")
            page.mouse.click(save_box["x"] + save_box["width"] / 2, save_box["y"] + save_box["height"] / 2)
            page.wait_for_timeout(3000)

    # 8. Check Distractor #1
    d1_final = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return 'Not found';
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return card.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
    }""")
    print("D1 after keyboard flow:", d1_final)

    page.screenshot(path="scratch/keyboard_d1_result.png")
    print("Saved scratch/keyboard_d1_result.png")
