import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome


def ensure_timer_running(page):
    print("Checking if timer is paused / modal is up...")
    st_btn = page.locator("button:has-text('Start timer')")
    if st_btn.count() > 0 and st_btn.first.is_visible():
        box = st_btn.first.bounding_box()
        if box:
            print("Clicking Start timer button at", box)
            page.mouse.click(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
            page.wait_for_timeout(1000)
    
    # Also check if top bar has play button to resume
    play_btn = page.evaluate("""() => {
        // Find timer in header
        const all = Array.from(document.querySelectorAll('header *, div[class*="header"] *'));
        const timerText = all.find(e => e.innerText && e.innerText.match(/\\d+:\\d+:\\d+\\s*\\/\\s*\\d+:\\d+:\\d+/));
        if (timerText) {
            const container = timerText.parentElement;
            const btn = container ? container.querySelector('button') : null;
            if (btn) {
                // If it's a play button (paused), click it
                const svg = btn.querySelector('svg');
                return { hasBtn: true, html: btn.outerHTML };
            }
        }
        return { hasBtn: false };
    }""")
    print("Timer button state:", play_btn)

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.bring_to_front()
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # 1. Resume timer
    ensure_timer_running(page)
    page.wait_for_timeout(1000)

    # Screenshot to verify timer is running and no modal
    page.screenshot(path="scratch/timer_running_check.png")

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

    # Check if timer modal popped up again
    ensure_timer_running(page)

    # 3. Click Edit on Distractor #1
    edit_box = page.evaluate("""() => {
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
    print("Edit box:", edit_box)
    if edit_box:
        page.mouse.click(edit_box["x"] + edit_box["width"] / 2, edit_box["y"] + edit_box["height"] / 2)
        page.wait_for_timeout(1000)

    ensure_timer_running(page)

    # 4. Fill 85 and click commit
    fill_res = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: "No Cancel button" };

        let p = cancelBtn;
        while (p && !p.querySelector('textarea, input[type="text"]') && p !== document.body) {
            p = p.parentElement;
        }
        const ta = p ? p.querySelector('textarea, input[type="text"]') : null;
        if (!ta) return { error: "No textarea" };

        // Fill 85
        const setVal = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value')?.set ||
                       Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value')?.set;
        if (setVal) setVal.call(ta, '85');
        else ta.value = '85';
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        // Click commit
        const commitBtn = Array.from(cancelBtn.parentElement.querySelectorAll('button')).find(b => b !== cancelBtn);
        if (!commitBtn) return { error: "No commit button" };
        commitBtn.click();
        return { success: true, newVal: ta.value };
    }""")
    print("Fill & commit result:", fill_res)
    page.wait_for_timeout(2000)

    # 5. Click Save
    save_res = page.evaluate("""() => {
        const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save');
        if (saveBtn) {
            saveBtn.click();
            return 'Clicked Save';
        }
        return 'No Save';
    }""")
    print("Save:", save_res)
    page.wait_for_timeout(3000)

    # 6. Verify Distractor #1 now
    d1_val = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return 'Not found';
        let card = el;
        for (let i = 0; i < 4; i++) if (card.parentElement) card = card.parentElement;
        return card.innerText.split('\\n').map(s => s.trim()).filter(Boolean);
    }""")
    print("Distractor #1 lines:", d1_val)

    page.screenshot(path="scratch/verified_timer_and_d1.png")
    print("Saved scratch/verified_timer_and_d1.png")
