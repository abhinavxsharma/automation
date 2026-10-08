import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])
    page.wait_for_timeout(1000)

    # Search for headings
    headings = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const matches = all.filter(el => {
            const t = el.innerText || '';
            return (t.includes('detailed description') || t.includes('Science Judge')) && el.children.length === 0;
        }).map(el => ({
            tag: el.tagName,
            text: el.innerText.trim(),
            hasEditBtnNear: !!el.closest('div')?.querySelector('button[aria-label="Edit this step"]')
        }));
        return matches;
    }""")

    print("Found matching headings:", headings)
