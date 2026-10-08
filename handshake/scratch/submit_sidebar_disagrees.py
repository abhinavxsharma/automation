import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "handshake/scratch")
from chrome_helper import PORT, ensure_chrome

PROMPT_CHECKER_REASON = (
    "The circuit diagram is an original internal lab image uploaded directly in Step 7 "
    "as the authoritative source of the circuit topology. External publication URL/DOI is N/A "
    "for original lab diagrams per Project Lumière guidelines."
)

SCIENCE_JUDGE_REASON = (
    "The prompt explicitly instructs to determine the fully simplified Boolean expression for output Q "
    "in terms of inputs A, B, and C from the circuit image, and to return the final answer as a single "
    "Boolean expression for Q using standard Boolean notation. The required output Q and simplification "
    "are completely and unambiguously defined."
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

    # 2. Check if a 'Reason for disagreeing' textarea is currently open
    submitted_first = page.evaluate("""(reasonText) => {
        const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
        if (!ta) return false;
        
        // Fill reason
        const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
        nativeSetter.call(ta, reasonText);
        ta.dispatchEvent(new Event('input', { bubbles: true }));
        ta.dispatchEvent(new Event('change', { bubbles: true }));
        
        // Find submit button in parent
        const p = ta.parentElement;
        const subBtn = p.querySelector(\"button[aria-label='Submit'], button[type='submit'], button:not([disabled])\");
        if (subBtn) {
            subBtn.click();
            return true;
        }
        return false;
    }""", PROMPT_CHECKER_REASON)
    print("Submitted first disagree reason:", submitted_first)
    page.wait_for_timeout(2000)

    # Dismiss timer if it popped up
    page.evaluate("""() => {
        const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Start timer'));
        if (btn) btn.click();
    }""")
    page.wait_for_timeout(500)

    # 3. Check remaining Disagree buttons in sidebar
    disagree_count = page.evaluate("""() => {
        return document.querySelectorAll(\"button[aria-label='Disagree']\").length;
    }""")
    print("Remaining Disagree buttons count:", disagree_count)

    # If there is another Disagree button, click it and fill the Science Judge reason
    if disagree_count > 0:
        opened_second = page.evaluate("""() => {
            const btn = document.querySelector(\"button[aria-label='Disagree']\");
            if (btn) {
                btn.scrollIntoView({ behavior: 'instant', block: 'center' });
                btn.click();
                return true;
            }
            return false;
        }""")
        print("Opened second Disagree form:", opened_second)
        page.wait_for_timeout(1500)

        submitted_second = page.evaluate("""(reasonText) => {
            const ta = document.querySelector(\"textarea[placeholder='Reason for disagreeing']\");
            if (!ta) return false;
            
            const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
            nativeSetter.call(ta, reasonText);
            ta.dispatchEvent(new Event('input', { bubbles: true }));
            ta.dispatchEvent(new Event('change', { bubbles: true }));
            
            const p = ta.parentElement;
            const subBtn = p.querySelector(\"button[aria-label='Submit'], button[type='submit'], button:not([disabled])\");
            if (subBtn) {
                subBtn.click();
                return true;
            }
            return false;
        }""", SCIENCE_JUDGE_REASON)
        print("Submitted second disagree reason:", submitted_second)
        page.wait_for_timeout(2000)

    # 4. Check feedback sidebar status
    sidebar_info = page.evaluate("""() => {
        const bodyText = document.body.innerText;
        const fbIdx = bodyText.indexOf('Feedback');
        return fbIdx !== -1 ? bodyText.slice(fbIdx, fbIdx + 600) : 'No Feedback found';
    }""")
    print("\n--- SIDEBAR STATUS ---")
    print(sidebar_info)

    page.screenshot(path="handshake/scratch/sidebar_after_disagree_submits.png")
    print("Saved screenshot to handshake/scratch/sidebar_after_disagree_submits.png")
