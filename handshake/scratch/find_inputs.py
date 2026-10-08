import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]

    inputs = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('input, textarea, [contenteditable="true"]')).map(el => ({
            tag: el.tagName,
            type: el.type,
            placeholder: el.placeholder,
            aria: el.getAttribute('aria-label'),
            val: el.value || el.innerText,
            visible: el.offsetParent !== null
        }));
    }""")
    for i, inp in enumerate(inputs):
        print(f"Input {i}:", inp)
