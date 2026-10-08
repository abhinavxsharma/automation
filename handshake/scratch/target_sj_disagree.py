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

    # 1. Dismiss modal
    page.evaluate("""() => {
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();
    }""")
    page.wait_for_timeout(1000)

    # 2. Inspect Disagree buttons and click the one inside Science Judge
    res = page.evaluate("""() => {
        const btns = Array.from(document.querySelectorAll(\"button[aria-label='Disagree']\"));
        const info = btns.map((b, i) => {
            let p = b.parentElement;
            while (p && p.innerText && !p.innerText.includes('Finding number') && p !== document.body) {
                p = p.parentElement;
            }
            return {
                i,
                visible: b.offsetWidth > 0,
                text: p ? p.innerText.slice(0, 150).replace(/\\n+/g, ' ') : null
            };
        });
        
        // Find the one for Science Judge
        const sjIdx = info.findIndex(item => item.text && item.text.includes('Science Judge'));
        if (sjIdx !== -1) {
            btns[sjIdx].click();
            return { clickedIdx: sjIdx, info };
        }
        return { error: 'No Science Judge Disagree button', info };
    }""")
    print("Click result:\n", json.dumps(res, indent=2))
    page.wait_for_timeout(1500)

    # 3. Check if textarea appeared
    ta_info = page.evaluate("""(reasonText) => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], textarea\");
        if (!ta) return { error: 'No textarea' };

        const proto = window.HTMLTextAreaElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        let cur = ta.parentElement;
        while (cur && cur.querySelectorAll('button').length === 0 && cur !== document.body) {
            cur = cur.parentElement;
        }
        const btns = Array.from(cur.querySelectorAll('button'));
        if (btns.length > 0) {
            btns[btns.length - 1].click();
            return { submitted: true, value: ta.value.slice(0, 50) };
        }
        return { submitted: false, btnsCount: btns.length };
    }""", REASON)
    print("Textarea & submit result:\n", json.dumps(ta_info, indent=2))
    page.wait_for_timeout(2000)

    # 4. Final check
    sidebar_text = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("\n--- SIDEBAR STATUS ---")
    print(sidebar_text)

    page.screenshot(path="handshake/scratch/after_sj_disagree_submitted_verified.png")
    print("Saved screenshot to handshake/scratch/after_sj_disagree_submitted_verified.png")
