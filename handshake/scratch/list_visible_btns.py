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
    page.wait_for_timeout(1000)

    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, i) => ({
            i,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0 && b.offsetHeight > 0
        })).filter(b => b.visible);
    }""")
    print("Visible buttons count:", len(btns))
    for b in btns:
        if b["text"] or b["aria"]:
            print(f"[{b['i']}] text={b['text']!r}, aria={b['aria']!r}")
