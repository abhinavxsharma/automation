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

    # 1. Dismiss modal
    page.evaluate("""() => {
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();
    }""")
    page.wait_for_timeout(1000)

    dom_info = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
        return btns.map((b, i) => {
            let chain = [];
            let cur = b;
            for (let depth = 0; depth < 6; depth++) {
                if (cur) {
                    chain.push({
                        tag: cur.tagName,
                        classes: cur.className,
                        text: (cur.innerText || '').slice(0, 100).replace(/\\n+/g, ' ')
                    });
                    cur = cur.parentElement;
                }
            }
            return { i, chain };
        });
    }""")
    print("DOM Info:\n", json.dumps(dom_info, indent=2))
