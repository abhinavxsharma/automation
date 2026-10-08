import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # Check body text around Feedback
    full_text = page.evaluate("() => document.body.innerText")
    fb_start = full_text.find("Feedback")
    if fb_start != -1:
        print("FEEDBACK SECTION:\n", full_text[fb_start:])
    else:
        print("Feedback not found in body text")

    # Check top banner
    banner = page.evaluate("""() => {
        const alert = document.querySelector('div[role="alert"], .bg-red-50, .border-red-200');
        return alert ? alert.innerText : 'No alert div found';
    }""")
    print("Top Alert:", banner)

    # Check Distractor #1 field
    d1 = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const el = all.find(e => e.innerText && e.innerText.trim() === 'Distractor #1:' && e.children.length === 0);
        if (!el) return 'Not found';
        let c = el;
        for (let i = 0; i < 4; i++) if (c.parentElement) c = c.parentElement;
        return c.innerText.replace(/\\n/g, ' ');
    }""")
    print("Distractor #1:", d1)

    page.screenshot(path="scratch/sidebar_and_banner_live.png")
    print("Saved scratch/sidebar_and_banner_live.png")
