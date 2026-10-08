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
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Scroll to Distractor #1
    print("Scrolling to Distractor #1...")
    scroll_res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return { error: "Leaf not found" };

        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        card.scrollIntoView({ behavior: 'instant', block: 'center' });

        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        return {
            found: true,
            hasEditBtn: !!editBtn
        };
    }""")
    print("Scroll result:", scroll_res)
    page.wait_for_timeout(1000)

    # 3. Click the edit button
    print("Clicking edit button...")
    click_res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        if (editBtn) {
            editBtn.click();
            return { clicked: true };
        }
        return { clicked: false };
    }""")
    print("Click edit result:", click_res)

    # 4. Wait for Cancel button to appear in the DOM
    print("Waiting for Cancel button...")
    cancel_found = False
    for _ in range(10):
        cancel_found = page.evaluate("() => Array.from(document.querySelectorAll('button')).some(b => b.innerText.trim() === 'Cancel')")
        if cancel_found:
            break
        page.wait_for_timeout(500)

    print("Cancel button found:", cancel_found)
    page.screenshot(path="scratch/flow_cancel_state.png")

    if not cancel_found:
        print("Error: Cancel button did not appear")
        sys.exit(1)

    # 5. Fill 85 and commit
    print("Filling 85 and clicking commit...")
    commit_action = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };

        // Find parent container with the input
        let p = cancelBtn;
        while (p && !p.querySelector('textarea, input[type="text"]') && p !== document.body) {
            p = p.parentElement;
        }
        const ta = p ? p.querySelector('textarea, input[type="text"]') : null;
        if (!ta) return { error: "No input found" };

        // Set value 85
        const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                       Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        if (setVal) {
            setVal.call(ta, '85');
        } else {
            ta.value = '85';
        }
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        // Find commit button (sibling of Cancel)
        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (!commitBtn) return { error: "No commit button next to Cancel" };

        commitBtn.click();
        return { success: true, newVal: ta.value };
    }""")
    print("Commit action:", commit_action)
    page.wait_for_timeout(2000)

    # 6. Click top Save
    print("Clicking top Save...")
    save_res = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Clicked Save';
        }
        return 'No Save button';
    }""")
    print("Save result:", save_res)
    page.wait_for_timeout(2500)

    # 7. Check verified Distractor #1 text
    verified = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return card.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
    }""")
    print("Distractor #1 verified lines:", verified)

    page.screenshot(path="scratch/flow_d1_saved.png")
    print("Saved scratch/flow_d1_saved.png")
