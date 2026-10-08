import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # 1. Dismiss timer modal with mouse
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Click button[aria-label="Disagree"]
    disagree_btn = page.locator("button[aria-label='Disagree']").first
    print("Disagree button visible:", disagree_btn.is_visible())
    if disagree_btn.is_visible():
        print("Clicking Disagree button...")
        disagree_btn.click()
        page.wait_for_timeout(2000)

    # 3. Check what appeared (any textarea, input, or did counter change?)
    state_after = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        const inps = Array.from(document.querySelectorAll('textarea, input')).filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && i.type !== 'radio';
        }).map(i => ({
            tag: i.tagName,
            placeholder: i.placeholder,
            value: i.value,
            rect: i.getBoundingClientRect()
        }));

        let sidebarText = '';
        const fbIdx = bodyText.indexOf('Feedback');
        if (fbIdx !== -1) {
            sidebarText = bodyText.slice(fbIdx, fbIdx + 600);
        }

        return {
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? nextBtn.innerText.trim() : null,
            submitBtn: submitBtn ? { text: submitBtn.innerText.trim(), disabled: submitBtn.disabled } : null,
            inputs: inps,
            sidebarText
        };
    }""")
    print("State after Disagree click:\n", json.dumps(state_after, indent=2))

    page.screenshot(path="scratch/after_disagree_click.png")
    print("Saved scratch/after_disagree_click.png")
