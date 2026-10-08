import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    radios = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('[role="radio"], input[type="radio"], label, button'));
        return els.map(e => ({
            tag: e.tagName,
            role: e.getAttribute('role'),
            text: e.innerText,
            cls: e.className,
            ariaChecked: e.getAttribute('aria-checked')
        })).filter(e => e.text && (e.text.includes('Integer') || e.text.includes('Decimal')));
    }""")
    for r in radios:
        print("Radio match:", r)
