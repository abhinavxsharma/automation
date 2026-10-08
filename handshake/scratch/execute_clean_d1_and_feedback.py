import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Dismiss timer modal via JS click
    dismissed = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) {
            st.click();
            return 'Clicked Start timer';
        }
        return 'No timer modal';
    }""")
    print("Modal check:", dismissed)
    page.wait_for_timeout(1000)

    # 2. Check if Cancel is visible. If not, click Edit this step on Distractor #1
    edit_state = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (cancelBtn) {
            return { hasCancel: true };
        }

        // Find Distractor #1 card
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return { error: "No Distractor #1 leaf found" };

        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        card.scrollIntoView({ behavior: 'instant', block: 'center' });

        const editBtn = card.querySelector('button[aria-label="Edit this step"]');
        if (editBtn) {
            editBtn.click();
            return { clickedEdit: true };
        }
        return { error: "No edit button found on card" };
    }""")
    print("Edit state:", edit_state)
    page.wait_for_timeout(1000)

    # 3. Now fill 85 and click commit via JS
    commit_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button found after edit click" };

        // Find textarea or input near cancelBtn
        let p = cancelBtn;
        while (p && !p.querySelector('textarea, input[type="text"]') && p !== document.body) {
            p = p.parentElement;
        }
        const ta = p ? p.querySelector('textarea, input[type="text"]') : null;
        if (!ta) return { error: "No input found near Cancel" };

        const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                       Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        if (setVal) {
            setVal.call(ta, '85');
        } else {
            ta.value = '85';
        }
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (!commitBtn) return { error: "No commit button next to Cancel" };

        commitBtn.click();
        return { success: true, newVal: ta.value };
    }""")
    print("Commit result:", commit_res)
    page.wait_for_timeout(1500)

    # 4. Click top Save via JS
    saved = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Save clicked';
        }
        return 'No Save button';
    }""")
    print("Top save:", saved)
    page.wait_for_timeout(2000)

    # 5. Inspect the current feedback sidebar & banner
    status = page.evaluate("""() => {
        const allText = document.body.innerText;
        const bannerLine = allText.split('\\n').find(l => l.includes('sent back') || l.includes('Distractor'));
        const counter = allText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        return {
            bannerLine,
            counter: counter ? counter[0] : null,
            submitBtn: submitBtn ? {
                text: submitBtn.innerText.trim(),
                disabled: submitBtn.disabled,
                classes: submitBtn.className
            } : null
        };
    }""")
    print("Post-save status:", status)

    page.screenshot(path="scratch/step_executed_clean.png")
    print("Saved scratch/step_executed_clean.png")
