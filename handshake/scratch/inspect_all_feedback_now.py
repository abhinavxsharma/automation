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
    page.wait_for_selector("button:has-text('Save')", timeout=15000)

    # Dismiss timer if visible
    btn = page.locator("button:has-text('Start timer')").first
    if btn.is_visible():
        btn.click()
        page.wait_for_timeout(500)

    # Find the feedback sidebar container
    res = page.evaluate("""() => {
        // Let's find any element containing 'Feedback'
        const allElements = Array.from(document.querySelectorAll('*'));
        const fbEl = allElements.find(e => e.children.length === 0 && e.innerText && e.innerText.trim() === 'Feedback');
        
        let container = null;
        if (fbEl) {
            let cur = fbEl;
            while (cur && cur !== document.body) {
                if (cur.innerText && cur.innerText.includes('items addressed')) {
                    container = cur;
                    break;
                }
                cur = cur.parentElement;
            }
        }
        
        const tabs = container ? Array.from(container.querySelectorAll('*')).filter(e => {
            const t = e.innerText ? e.innerText.trim() : '';
            return t === 'All' || t.startsWith('Needs attention');
        }).map(e => ({ tag: e.tagName, text: e.innerText, classes: e.className })) : [];

        return {
            containerText: container ? container.innerText : null,
            tabs
        };
    }""")
    print("Container Text:\n", res["containerText"])
    print("Tabs found:\n", json.dumps(res["tabs"], indent=2))

    # Try clicking the 'All' tab if found
    clicked = page.evaluate("""() => {
        const els = Array.from(document.querySelectorAll('*')).filter(e => e.innerText && e.innerText.trim() === 'All');
        // pick deepest
        if (els.length > 0) {
            const target = els[els.length - 1];
            target.click();
            return true;
        }
        return false;
    }""")
    print("Clicked 'All':", clicked)
    page.wait_for_timeout(1000)

    # After clicking All
    afterText = page.evaluate("""() => {
        const allElements = Array.from(document.querySelectorAll('*'));
        const fbEl = allElements.find(e => e.children.length === 0 && e.innerText && e.innerText.trim() === 'Feedback');
        let cur = fbEl;
        while (cur && cur !== document.body) {
            if (cur.innerText && cur.innerText.includes('items addressed')) {
                return cur.innerText;
            }
            cur = cur.parentElement;
        }
        return null;
    }""")
    print("\nContainer Text after clicking All:\n", afterText)
    page.screenshot(path="handshake/scratch/after_all_tab_clicked.png")
