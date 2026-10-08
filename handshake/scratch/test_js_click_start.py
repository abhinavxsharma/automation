import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Click Start timer if open
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const st = btns.find(b => b.innerText.includes('Start timer'));
        if (st) st.click();
    }""")
    page.wait_for_timeout(1000)

    # Click Start in Feedback panel via JS evaluate!
    clicked_start = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll('button'));
        const startBtn = btns.find(b => b.innerText.trim() === 'Start' && b.offsetParent !== null);
        if (startBtn) {
            startBtn.click();
            return true;
        }
        return false;
    }""")
    print("Clicked Start via evaluate:", clicked_start)
    page.wait_for_timeout(1500)

    page.screenshot(path="scratch/after_js_click_start.png")

    fb_text = page.evaluate("""() => {
        const body = document.body.innerText;
        const start = body.indexOf('Feedback');
        return start !== -1 ? body.slice(start, start + 1000) : '';
    }""")
    print("Feedback text:\n", fb_text)
