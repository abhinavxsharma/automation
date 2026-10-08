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

    # 2. Wait for quality check to complete (up to 10s)
    for i in range(10):
        qc = page.evaluate("() => document.body ? document.body.innerText.includes('Running quality check') : false")
        if not qc:
            print(f"Quality check completed after {i}s")
            break
        page.wait_for_timeout(1000)

    # 3. Check status before clicking Next
    status_before = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const bannerLine = bodyText.split('\\n').find(l => l.includes('sent back') || l.includes('Distractor'));
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');

        return {
            bannerLine,
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? { text: nextBtn.innerText.trim(), disabled: nextBtn.disabled, classes: nextBtn.className } : null,
            submitBtn: submitBtn ? { text: submitBtn.innerText.trim(), disabled: submitBtn.disabled, classes: submitBtn.className } : null
        };
    }""")
    print("Status before Next click:\n", json.dumps(status_before, indent=2))

    # 4. Click Next button
    print("Clicking Next button...")
    next_res = page.evaluate("""() => {
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        if (nextBtn) {
            nextBtn.click();
            return { clicked: true, text: nextBtn.innerText.trim() };
        }
        return { clicked: false, error: "No Next button found" };
    }""")
    print("Next click result:", next_res)
    page.wait_for_timeout(2000)

    # 5. Check status after clicking Next
    status_after = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const counter = bodyText.match(/\\d+\\s*\\/\\s*\\d+\\s*items addressed/i);
        const nextBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Next');
        const submitBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Submit task');
        
        let sidebarText = '';
        const fbIdx = bodyText.indexOf('Feedback');
        if (fbIdx !== -1) {
            sidebarText = bodyText.slice(fbIdx, fbIdx + 600);
        }

        return {
            counter: counter ? counter[0] : null,
            nextBtn: nextBtn ? { text: nextBtn.innerText.trim(), disabled: nextBtn.disabled } : null,
            submitBtn: submitBtn ? { text: submitBtn.innerText.trim(), disabled: submitBtn.disabled } : null,
            sidebarText
        };
    }""")
    print("Status after Next click:\n", json.dumps(status_after, indent=2))

    page.screenshot(path="scratch/after_clicking_next.png")
    print("Saved scratch/after_clicking_next.png")
