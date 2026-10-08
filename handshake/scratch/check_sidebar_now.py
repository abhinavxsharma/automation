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

    # Get sidebar text
    bodyText = page.evaluate("() => document.body.innerText")
    fbIdx = bodyText.find("Feedback")
    if fbIdx != -1:
        print("Feedback sidebar text:\n", bodyText[fbIdx:fbIdx + 1200])

    # Also check what buttons are in the sidebar
    sb_btns = page.evaluate("""() => {
        const all = Array.from(document.querySelectorAll('*'));
        const fbEl = all.find(e => e.children.length === 0 && e.innerText && e.innerText.trim() === 'Feedback');
        if (!fbEl) return [];
        let cur = fbEl;
        while (cur && !cur.innerText.includes('items addressed') && cur !== document.body) {
            cur = cur.parentElement;
        }
        return Array.from(cur.querySelectorAll('button')).map(b => ({
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0
        })).filter(b => b.visible);
    }""")
    print("Sidebar buttons:\n", sb_btns)
