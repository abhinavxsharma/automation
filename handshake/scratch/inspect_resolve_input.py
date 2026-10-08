import sys

from playwright.sync_api import sync_playwright

sys.path.insert(0, "scratch")
from chrome_helper import PORT, ensure_chrome

with sync_playwright() as p:
    ensure_chrome()
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = next((pg for pg in browser.contexts[0].pages if "/task/1520c7f4" in pg.url), browser.contexts[0].pages[0])

    # Inspect inputs inside feedback panel
    inputs = page.evaluate("""() => {
        const panel = Array.from(document.querySelectorAll('*')).find(el => el.innerText && el.innerText.startsWith('Feedback') && el.clientWidth > 250);
        if (!panel) return { error: "No panel" };

        const allInputs = Array.from(panel.querySelectorAll('input, textarea')).map(i => ({
            tag: i.tagName,
            placeholder: i.placeholder,
            value: i.value,
            rect: i.getBoundingClientRect()
        }));

        const sendBtns = Array.from(panel.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            rect: b.getBoundingClientRect(),
            disabled: b.disabled
        }));

        return {
            inputs: allInputs,
            buttons: sendBtns
        };
    }""")

    print("Resolve input info:", inputs)
