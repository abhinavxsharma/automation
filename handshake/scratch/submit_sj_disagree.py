import json
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

REASON = (
    "The prompt is fully self-contained and explicitly requests: 'Determine the fully simplified Boolean expression "
    "for the output Q in terms of the independent inputs A, B, and C from the provided circuit image' and 'Return the "
    "final answer as a single Boolean expression for Q, using standard Boolean notation with no units or extra quantities.' "
    "Both the requested output Q and the simplification are completely and unambiguously defined from the prompt and the provided circuit topology."
)

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

    # 2. Inspect the active input with placeholder 'Reason for disagreeing'
    input_info = page.evaluate("""(reasonText) => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], input[placeholder='Reason for disagreeing']\");
        if (!ta) return { error: 'No input with placeholder Reason for disagreeing' };
        
        // Fill the reason
        const proto = ta.tagName === 'TEXTAREA' ? window.HTMLTextAreaElement.prototype : window.HTMLInputElement.prototype;
        const nativeSetter = Object.getOwnPropertyDescriptor(proto, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));

        // Find the submit button next to or inside this input container
        let container = ta.parentElement;
        const btns = Array.from(container.querySelectorAll('button'));
        
        return {
            tag: ta.tagName,
            value: ta.value.slice(0, 50),
            btns: btns.map(b => ({
                text: b.innerText,
                aria: b.getAttribute('aria-label'),
                disabled: b.disabled,
                outerHTML: b.outerHTML
            }))
        };
    }""", REASON)
    print("Input and submit buttons:\n", json.dumps(input_info, indent=2))

    # 3. Click the up-arrow submit button
    submitted = page.evaluate("""() => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing'], input[placeholder='Reason for disagreeing']\");
        if (!ta) return false;
        
        let container = ta.parentElement;
        // The submit button is typically the last button or has an arrow SVG or submit
        const btns = Array.from(container.querySelectorAll('button'));
        if (btns.length > 0) {
            const sub = btns[btns.length - 1];
            sub.click();
            return true;
        }
        return false;
    }""")
    print("Clicked submit button:", submitted)
    page.wait_for_timeout(2000)

    # 4. Check feedback sidebar status and screenshot
    sidebar_text = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'None';
    }""")
    print("\n--- SIDEBAR AFTER SUBMISSION ---")
    print(sidebar_text)

    page.screenshot(path="handshake/scratch/after_sj_disagree_submitted.png")
    print("Saved screenshot to handshake/scratch/after_sj_disagree_submitted.png")
