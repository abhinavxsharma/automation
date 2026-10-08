import json
import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    # 1. Dismiss timer if visible
    st = page.locator("button:has-text('Start timer')").first
    if st.is_visible():
        b = st.bounding_box()
        if b:
            print("Clicking Start timer...")
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Open sidebar if not already open
    close_btn = page.locator("button[aria-label='Close']").first
    if not close_btn.is_visible():
        print("Sidebar is closed. Clicking Feedback toggle...")
        page.locator("button[aria-label='Feedback']").first.click()
        page.wait_for_timeout(1500)

    # 3. Check Disagree button
    d_btn = page.locator("button[aria-label='Disagree']").first
    print("Disagree button count:", page.locator("button[aria-label='Disagree']").count())
    print("Disagree button is_visible:", d_btn.is_visible())

    if d_btn.is_visible():
        print("Clicking Disagree with force=True...")
        d_btn.click(force=True)
        page.wait_for_timeout(2000)

    # 4. Inspect state
    info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const sub = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        const next = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        
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
            hasNext: !!next,
            nextDisabled: next ? next.disabled : null,
            hasSubmit: !!sub,
            submitDisabled: sub ? sub.disabled : null,
            inputs: inps,
            sidebarText
        };
    }""")
    print("Post-click info:\n", json.dumps(info, indent=2))

    page.screenshot(path="scratch/after_open_and_disagree.png")
    print("Saved scratch/after_open_and_disagree.png")
