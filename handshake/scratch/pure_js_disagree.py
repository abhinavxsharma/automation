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

    # 1. Dismiss modal + click Disagree via JS
    res = page.evaluate("""() => {
        // Dismiss timer modal if present
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();
        
        // Find Disagree button
        const btn = document.querySelector(\"button[aria-label='Disagree']\");
        if (btn) {
            btn.click();
            return { clicked: true };
        }
        return { clicked: false, hasBtn: !!btn };
    }""")
    print("JS click Disagree result:", res)
    page.wait_for_timeout(1000)

    # 2. Fill reason and submit via JS
    submit_res = page.evaluate("""(reasonText) => {
        // Dismiss timer modal if present
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();

        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], input[placeholder='Reason for disagreeing']\");
        if (!ta) return { error: 'No reason input found' };

        const proto = ta.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
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
            const subBtn = btns[btns.length - 1];
            subBtn.click();
            return { submitted: true, btnText: subBtn.innerText, btnAria: subBtn.getAttribute('aria-label') };
        }
        return { submitted: false, btnsCount: btns.length };
    }""", REASON)
    print("JS submit reason result:", submit_res)
    page.wait_for_timeout(2000)

    # 3. Check sidebar status
    sidebar_info = page.evaluate("""() => {
        // Dismiss timer modal if present
        const stBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (stBtn) stBtn.click();

        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("\n--- SIDEBAR STATUS ---")
    print(sidebar_info)

    page.screenshot(path="handshake/scratch/after_pure_js_disagree.png")
    print("Saved screenshot to handshake/scratch/after_pure_js_disagree.png")
