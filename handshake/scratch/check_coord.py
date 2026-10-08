import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    
    # Inspect element at 945, 205
    el_info = page.evaluate("""() => {
        const el = document.elementFromPoint(945, 205);
        if (!el) return 'No element at 945, 205';
        let b = el;
        const chain = [];
        while (b && b !== document.body) {
            chain.push({
                tag: b.tagName,
                className: b.className,
                aria: b.getAttribute('aria-label') || '',
                title: b.getAttribute('title') || '',
                html: b.outerHTML.slice(0, 80)
            });
            b = b.parentElement;
        }
        return chain;
    }""")
    print("Element chain at 945, 205:\n", el_info)
