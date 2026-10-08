import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    btn_info = page.evaluate("""() => {
        const ta = document.querySelector('textarea[placeholder*="resolve reason"]');
        if (!ta) return 'No textarea';

        let p = ta.parentElement;
        while (p && p !== document.body) {
            const btns = Array.from(p.querySelectorAll('button'));
            if (btns.length > 0) {
                return btns.map(b => ({
                    aria: b.getAttribute('aria-label'),
                    className: b.className,
                    html: b.outerHTML.slice(0, 150),
                    rect: b.getBoundingClientRect()
                }));
            }
            p = p.parentElement;
        }
        return 'No button in ancestors';
    }""")

    print("Buttons near resolve textarea:\n", btn_info)
