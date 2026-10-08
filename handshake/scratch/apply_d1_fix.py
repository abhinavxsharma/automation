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

    # 2. Find and scroll Distractor #1 card into view
    print("Locating Distractor #1 card...")
    card_info = page.evaluate("""() => {
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
    print("Distractor #1 location:", card_info)
    page.wait_for_timeout(1000)

    # 3. Click the edit button on Distractor #1
    print("Clicking Edit this step...")
    edit_clicked = page.evaluate("""() => {
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
    print("Edit clicked:", edit_clicked)
    page.wait_for_timeout(1000)

    # 4. Fill 85 into the input/textarea and click commit
    print("Setting value to 85 and committing...")
    commit_res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;

        const ta = card.querySelector('textarea, input[type="text"]');
        if (!ta) return { error: "No textarea/input in card" };

        // React controlled input setter
        const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                       Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        if (setVal) {
            setVal.call(ta, '85');
        } else {
            ta.value = '85';
        }
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        const cancelBtn = Array.from(card.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No cancel button found" };

        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (commitBtn) {
            commitBtn.click();
            return { success: true, newVal: ta.value, commitBtnHtml: commitBtn.outerHTML };
        }
        return { error: "No commit button found" };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(1500)

    # 5. Click top Save button
    print("Clicking top Save button...")
    save_res = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Save clicked';
        }
        return 'Save not found';
    }""")
    print("Top save:", save_res)
    page.wait_for_timeout(2500)

    # 6. Verify Distractor #1 text now
    verified = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return card.innerText.split('\\n').map(s => s.trim()).filter(Boolean).slice(0, 4);
    }""")
    print("Distractor #1 lines now:", verified)

    page.screenshot(path="scratch/after_d1_applied.png")
    print("Saved scratch/after_d1_applied.png")
