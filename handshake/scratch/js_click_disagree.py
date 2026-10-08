import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # 1. Dismiss timer modal via JS if present
    st_clicked = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) {
            st.click();
            return true;
        }
        return false;
    }""")
    print("Dismissed timer via JS:", st_clicked)
    page.wait_for_timeout(1000)

    # 2. Check if sidebar is open, if not open it via JS
    opened_sb = page.evaluate("""() => {
        const closeBtn = document.querySelector('button[aria-label="Close"]');
        if (!closeBtn) {
            const fb = document.querySelector('button[aria-label="Feedback"]');
            if (fb) {
                fb.click();
                return 'Opened sidebar';
            }
            return 'No feedback button';
        }
        return 'Sidebar was already open';
    }""")
    print("Sidebar status:", opened_sb)
    page.wait_for_timeout(1500)

    # 3. Click Disagree button via JS
    disagree_clicked = page.evaluate("""() => {
        const d = document.querySelector('button[aria-label="Disagree"]');
        if (d) {
            d.click();
            return { success: true, aria: d.getAttribute('aria-label') };
        }
        return { success: false, error: 'No Disagree button found' };
    }""")
    print("Disagree click:", disagree_clicked)
    page.wait_for_timeout(2000)

    # 4. Check status after click
    post_info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        let sidebarText = '';
        const fbIdx = bodyText.indexOf('Feedback');
        if (fbIdx !== -1) {
            sidebarText = bodyText.slice(fbIdx, fbIdx + 600);
        }

        const inps = Array.from(document.querySelectorAll('textarea, input')).filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && i.type !== 'radio';
        }).map(i => ({
            tag: i.tagName,
            placeholder: i.placeholder,
            value: i.value,
            rect: i.getBoundingClientRect()
        }));

        return {
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? nextBtn.innerText.trim() : null,
            submitBtn: submitBtn ? { text: submitBtn.innerText.trim(), disabled: submitBtn.disabled } : null,
            inputs: inps,
            sidebarText
        };
    }""")
    print("Post-disagree info:\n", json.dumps(post_info, indent=2))

    page.screenshot(path="scratch/after_js_disagree.png")
    print("Saved scratch/after_js_disagree.png")
