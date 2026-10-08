import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # Dismiss timer modal via JS
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    tas = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('textarea, input, [contenteditable=\"true\"]')).map((el, i) => ({
            i,
            tag: el.tagName,
            type: el.type,
            placeholder: el.placeholder,
            value: (el.value || el.innerText || '').slice(0, 100),
            visible: el.offsetWidth > 0 && el.offsetHeight > 0
        })).filter(e => e.visible);
    }""")
    print("All visible inputs:\n", json.dumps(tas, indent=2))
