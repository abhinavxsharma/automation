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
            page.mouse.click(b["x"] + b["width"] / 2, b["y"] + b["height"] / 2)
            page.wait_for_timeout(1000)

    # 2. Check if sidebar is open by checking Close button
    close_btn = page.locator("button[aria-label='Close']").first
    if not close_btn.is_visible():
        print("Opening sidebar via Feedback button...")
        page.locator("button[aria-label='Feedback']").first.click()
        page.wait_for_timeout(1500)

    # 3. Check Disagree button
    disagree_btn = page.locator("button[aria-label='Disagree']").first
    print("Disagree button visible:", disagree_btn.is_visible())
    if disagree_btn.is_visible():
        box = disagree_btn.bounding_box()
        print("Clicking Disagree button at:", box)
        disagree_btn.click()
        page.wait_for_timeout(2000)

    # 4. Check DOM for inputs or changes
    info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const inps = Array.from(document.querySelectorAll('input, textarea')).filter(i => {
            const r = i.getBoundingClientRect();
            return r.width > 0 && r.height > 0 && i.type !== 'radio';
        }).map(i => ({
            tag: i.tagName,
            placeholder: i.placeholder,
            value: i.value,
            rect: i.getBoundingClientRect(),
            parentHtml: i.parentElement ? i.parentElement.outerHTML.substring(0, 100) : ''
        }));

        let sidebarText = '';
        const fbIdx = bodyText.indexOf('Feedback');
        if (fbIdx !== -1) {
            sidebarText = bodyText.slice(fbIdx, fbIdx + 600);
        }

        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');

        return {
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? { text: nextBtn.innerText.trim(), disabled: nextBtn.disabled } : null,
            submitBtn: submitBtn ? { text: submitBtn.innerText.trim(), disabled: submitBtn.disabled } : null,
            inputs: inps,
            sidebarText
        };
    }""")
    print("Post-click info:\n", json.dumps(info, indent=2))

    page.screenshot(path="scratch/after_disagree_proper.png")
    print("Saved scratch/after_disagree_proper.png")
