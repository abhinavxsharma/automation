import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss modal via JS
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Inspect Distractor #1 field and edit state
    d1_res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!d1) return { error: "No Distractor #1" };

        let c = d1;
        for (let i = 0; i < 4; i++) if (c.parentElement) c = c.parentElement;

        const ta = c.querySelector('textarea, input[type="text"]');
        const cancelBtn = Array.from(c.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        const editBtn = c.querySelector('button[aria-label="Edit this step"]');

        return {
            cardText: c.innerText.replace(/\\n/g, ' '),
            hasTa: !!ta,
            taVal: ta ? ta.value : null,
            hasCancel: !!cancelBtn,
            hasEditBtn: !!editBtn
        };
    }""")
    print("Distractor #1 initial state:", d1_res)

    # 3. If cancel is visible, textarea is open. If not, click edit
    if not d1_res.get("hasCancel"):
        print("Clicking edit on Distractor #1...")
        page.evaluate("""() => {
            const all = Array.from(document.querySelectorAll('*'));
            const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
            let c = d1;
            while (c && c !== document.body) {
                const btn = c.querySelector('button[aria-label="Edit this step"]');
                if (btn) {
                    btn.click();
                    break;
                }
                c = c.parentElement;
            }
        }""")
        page.wait_for_timeout(1000)

    # 4. Set value to exactly "85" and commit
    update_res = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let c = d1;
        for (let i = 0; i < 4; i++) if (c.parentElement) c = c.parentElement;

        const ta = c.querySelector('textarea, input[type="text"]');
        if (!ta) return { error: "No input/textarea in card" };

        const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                       Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        if (setVal) {
            setVal.call(ta, '85');
        } else {
            ta.value = '85';
        }
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        const cancelBtn = Array.from(c.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No cancel button" };
        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (commitBtn) {
            commitBtn.click();
            return { success: true, newVal: ta.value };
        }
        return { error: "No commit button" };
    }""")
    print("Update result:", update_res)
    page.wait_for_timeout(1500)

    # 5. Click top Save
    save_res = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Clicked Save';
        }
        return 'No Save button';
    }""")
    print("Top save:", save_res)
    page.wait_for_timeout(2000)

    # 6. Verify Distractor #1 text now
    final_d1 = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const d1 = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        let c = d1;
        for (let i = 0; i < 4; i++) if (c.parentElement) c = c.parentElement;
        return c.innerText.replace(/\\n/g, ' ');
    }""")
    print("Verified Distractor #1 in DOM:", final_d1)

    page.screenshot(path="scratch/d1_clean_85.png")
