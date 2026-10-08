import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

REASON = (
    "The prompt explicitly instructs to determine the fully simplified Boolean expression for output Q "
    "in terms of inputs A, B, and C from the provided circuit image, and to return the final answer as a single "
    "Boolean expression for Q using standard Boolean notation. The required output Q and simplification "
    "are completely and unambiguously defined from the prompt and the provided circuit topology."
)

ensure_chrome()
with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp(f"http://127.0.0.1:{PORT}")
    page = browser.contexts[0].pages[0]
    page.wait_for_selector("text=Project Lumière", timeout=15000)

    # 1. Dismiss modal using evaluate and wait for dialog to unmount
    page.evaluate("""() => {
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();
    }""")
    page.wait_for_timeout(1500)

    # 2. Check all buttons in the document
    btns = page.evaluate("""() => {
        return Array.from(document.querySelectorAll('button')).map((b, idx) => ({
            idx,
            text: b.innerText.trim(),
            aria: b.getAttribute('aria-label'),
            visible: b.offsetWidth > 0 && b.offsetHeight > 0
        })).filter(b => b.visible && (b.aria === 'Disagree' || (b.text && b.text.includes('Disagree')) || b.aria === 'Quality check'));
    }""")
    print("Matching buttons in DOM after dismissing modal:\n", json.dumps(btns, indent=2))

    # 3. Click the circle-slash Disagree button
    clicked = page.evaluate("""() => {
        const btn = document.querySelector(\"button[aria-label='Disagree']\");
        if (btn) {
            btn.click();
            return true;
        }
        return false;
    }""")
    print("Clicked Disagree button:", clicked)
    page.wait_for_timeout(1000)

    # 4. Fill the reason textarea
    filled = page.evaluate("""(reasonText) => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], textarea\");
        if (!ta) return false;
        
        const proto = window.HTMLTextAreaElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        return true;
    }""", REASON)
    print("Filled reason textarea:", filled)
    page.wait_for_timeout(500)

    # 5. Click the submit button inside the reason container
    submitted = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], textarea\");
        if (!ta) return false;
        
        let cur = ta.parentElement;
        while (cur && cur.querySelectorAll('button').length === 0 && cur !== document.body) {
            cur = cur.parentElement;
        }
        const btns = Array.from(cur.querySelectorAll('button'));
        if (btns.length > 0) {
            btns[btns.length - 1].click();
            return true;
        }
        return false;
    }""")
    print("Submitted Disagree form:", submitted)
    page.wait_for_timeout(2000)

    # 6. Read sidebar text and take screenshot
    sidebar_text = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("\n--- SIDEBAR STATUS ---")
    print(sidebar_text)

    page.screenshot(path="handshake/scratch/after_sj_disagree_step_by_step.png")
    print("Saved screenshot to handshake/scratch/after_sj_disagree_step_by_step.png")
