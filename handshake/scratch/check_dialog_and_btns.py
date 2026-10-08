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

    # 1. Dismiss timer modal via JS and wait for dialog to be gone
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1500)

    # Check if any dialog is still open
    has_dialog = page.evaluate("() => !!document.querySelector(\"[role='dialog']\")")
    print("Is dialog open:", has_dialog)

    # Find Disagree buttons
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\")).map((b, i) => ({
            i,
            text: b.innerText,
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0
        }));
    }""")
    print("Disagree buttons:", btns)
