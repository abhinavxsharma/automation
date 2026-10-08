from chrome_helper import PORT, ensure_chrome
from playwright.sync_api import sync_playwright

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    info = page.evaluate("""() => {
        const el = Array.from(document.querySelectorAll('*')).find(
            e => e.placeholder === 'Start typing...' || (e.innerText && e.innerText.includes('Start typing...'))
        );
        if (!el) return null;
        return {
            tagName: el.tagName,
            className: el.className,
            contentEditable: el.contentEditable,
            placeholder: el.getAttribute('placeholder'),
            outerHTML: el.outerHTML.slice(0, 300)
        };
    }""")
    print("Element info:", info)
