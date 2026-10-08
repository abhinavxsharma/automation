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

    # Dismiss timer modal
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(1000)

    # Click edit on step 23
    page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Edit this step']\"));
        if (btns[23]) {
            btns[23].scrollIntoView({ behavior: 'instant', block: 'center' });
            btns[23].click();
        }
    }""")
    page.wait_for_timeout(1500)

    # Inspect editor in step 23
    info = page.evaluate("""() => {
        const cancelBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Cancel');
        if (!cancelBtn) return { error: 'No cancel button' };
        
        let p = cancelBtn.parentElement;
        const btns = Array.from(p.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            outerHTML: b.outerHTML
        }));
        
        const ta = document.querySelector('textarea');
        return {
            taVal: ta ? ta.value : null,
            btns
        };
    }""")
    print("Step 23 editor info:\n", json.dumps(info, indent=2))
