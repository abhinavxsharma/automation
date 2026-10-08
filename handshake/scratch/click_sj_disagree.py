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

    # 1. Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Check the circle-slash buttons / Disagree buttons in the sidebar
    btns = page.evaluate("""() => {
        const allBtns = Array.from(document.querySelectorAll('button'));
        return allBtns.map((b, i) => ({
            i,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0,
            classes: b.className
        })).filter(b => b.visible && (b.aria === 'Disagree' || (b.text && b.text.includes('Disagree'))));
    }""")
    print("Found Disagree buttons:", btns)

    # Click the second one (Science Judge)
    if len(btns) > 1:
        print("Clicking Science Judge Disagree button...")
        page.evaluate("""() => {
            const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
            if (btns.length > 1) btns[1].click();
        }""")
        page.wait_for_timeout(1000)

        # Take screenshot to see what opened
        page.screenshot(path="handshake/scratch/after_sj_click.png")
        print("Saved handshake/scratch/after_sj_click.png")
